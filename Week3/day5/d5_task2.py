from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

from model import retrieve, build_prompt, embed_and_store
from functions import load_pdf, chunk_text
from groq_function import ask


app = FastAPI()


# Store conversations in memory
conversation_history = {}


# Request model
class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None


# Response model
class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    session_id: str


# PDF file
file_path = "article 2.pdf"

# Load PDF using pymupdf4llm
text = load_pdf(file_path)

# Create chunks
chunks = chunk_text(text)


# Create metadata
metadata_list = []

for i in range(len(chunks)):

    metadata_list.append({
        "source": file_path,
        "chunk_index": i
    })


# Qdrant collection
collection = "Agriculture Article"


# Store embeddings
embed_and_store(chunks,metadata_list,collection)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # Create a new session if session_id is not provided
    session_id = request.session_id

    if session_id is None:
        session_id = str(uuid4())

    # Create history for new session
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    # User query
    query = request.query


    # Retrieve relevant chunks
    retrieved_chunks = retrieve(query,collection,top_k=3)


    # Build RAG prompt
    prompt = build_prompt(query,retrieved_chunks)


    # Get previous conversation
    previous_messages = conversation_history[session_id]


    # Send prompt + previous messages to Groq
    answer = ask(prompt,previous_messages=previous_messages)


    # Save current conversation
    conversation_history[session_id].append(
        {
            "role": "user",
            "content": query
        }
    )

    conversation_history[session_id].append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # Keep only last 6 turns
    conversation_history[session_id] = (
        conversation_history[session_id][-12:]
    )


    # Get source metadata
    sources = []

    for chunk in retrieved_chunks:

        sources.append(
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }
        )


    return {
        "answer": answer,
        "sources": sources,
        "session_id": session_id
    }