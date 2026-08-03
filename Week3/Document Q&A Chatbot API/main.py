from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
import shutil
import tempfile
import hashlib    #Cache library

from app.ingestion import load_document, chunk_text
from app.embeddings import generate_embeddings , generate_query_embedding
from app.vector_store import create_collection, store_chunks ,search_similar_chunks
from app.llm import generate_answer , generate_answer_stream
from app.models import ChatRequest, ChatResponse, Source


# Create FastAPI app
app = FastAPI(
    title="Document Q&A Chatbot API",
    description="RAG-powered chatbot using Groq, Sentence Transformers, and Qdrant",
    version="1.0.0"
)

# Create Qdrant collection when application starts
create_collection()

@app.get("/")
def root():
    return { "message": "Document Q&A Chatbot API is running"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Upload a TXT or PDF document,
    chunk it, generate embeddings,
    and store the chunks in Qdrant.
    """

    # Validate file extension
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in [".txt", ".pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Only TXT and PDF files are supported."
        )

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False,suffix=file_extension) as temp_file:

            shutil.copyfileobj(file.file,temp_file)

            temp_file_path = temp_file.name

        # Load document
        text = load_document(temp_file_path)

        # Check if document contains text
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="The uploaded document is empty."
            )

        # Chunk document
        chunks = chunk_text(text)

        # Generate embeddings
        embeddings = generate_embeddings(chunks)

        # Store chunks and embeddings in Qdrant
        store_chunks(chunks=chunks,embeddings=embeddings,source_filename=file.filename)

        return {
            "message": "Document ingested successfully",
            "filename": file.filename,
            "chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

    finally:
        # Delete temporary file
        if "temp_file_path" in locals():
            Path(temp_file_path).unlink(missing_ok=True)




# Conversation history
conversation_history = {}
query_cache = {}

# Chat endpoint without streaming and with caching
@app.post("/chat",response_model=ChatResponse)
def chat(request: ChatRequest):

    # Get session ID
    session_id = request.session_id
    # Get user query
    query = request.query

    # Create cache key using session_id + query hash
    query_hash = hashlib.sha256(
        query.strip().lower().encode("utf-8")
    ).hexdigest()

    cache_key = (session_id, query_hash)

    # Return cached response if available
    if cache_key in query_cache:
        return query_cache[cache_key]

    # Get previous history
    history = conversation_history.get(session_id,[])

    # Keep only last 6 turns
    recent_history = history[-12:]

    # Generate embedding for user query
    query_embedding = generate_query_embedding(query)

    # Search Qdrant
    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=3
    )

    # Build context
    context_parts = []

    for result in results:
        context_parts.append(result.payload["text"])

    context = "\n\n".join(context_parts)

    # Generate answer using Groq
    answer = generate_answer(
        query=query,
        context=context,
        history=recent_history
    )

    sources = [
    Source(
        source=result.payload["source"],
        chunk_index=result.payload["chunk_index"]
    )
    for result in results
    ]

    # Create response
    response = ChatResponse(answer=answer,sources=sources)

    # Save current conversation
    conversation_history.setdefault(
            session_id,
            []
        ).extend(
            [
                {
                    "role": "user",
                    "content": query
                },
                {
                    "role": "assistant",
                    "content": answer
                }
            ]
        )
    
    # Save response in cache
    query_cache[cache_key] = response

    return response

# Streaming API
@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    session_id = request.session_id
    query = request.query

    # Get conversation history
    history = conversation_history.get(session_id, [])

    # Last 6 turns = 12 messages
    recent_history = history[-12:]

    # Generate query embedding
    query_embedding = generate_query_embedding(query)

    # Retrieve top 3 relevant chunks
    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=3
    )

    # Build context
    context_parts = [
        result.payload["text"]
        for result in results
    ]

    context = "\n\n".join(context_parts)

    # Generate streaming response
    return StreamingResponse(
        generate_answer_stream(
            query=query,
            context=context,
            history=recent_history
        ),
        media_type="text/plain"
    )
    
