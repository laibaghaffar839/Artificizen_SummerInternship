from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import tempfile

from app.ingestion import load_document, chunk_text
from app.embeddings import generate_embeddings
from app.vector_store import create_collection, store_chunks


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
