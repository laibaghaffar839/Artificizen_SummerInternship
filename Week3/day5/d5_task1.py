from fastapi import FastAPI
from pydantic import BaseModel

from functions import load_pdf, chunk_text
from model import embed_and_store, retrieve, build_prompt
from groq_function import ask


app = FastAPI()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]


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


# Chat API
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    query = request.query

    # Retrieve relevant chunks
    retrieved_chunks = retrieve(query,collection,top_k=3)

    # Build prompt
    prompt = build_prompt(query,retrieved_chunks)

    # Generate answer
    answer = ask(prompt)

    # Get source metadata
    sources = []

    for chunk in retrieved_chunks:

        sources.append({
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"]
        })

    return {
        "answer": answer,
        "sources": sources
    }