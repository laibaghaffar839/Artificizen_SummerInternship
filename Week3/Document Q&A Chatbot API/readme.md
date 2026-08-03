# Document Q&A Chatbot API

A simple RAG-powered Document Question-Answering Chatbot API built with FastAPI.
The chatbot allows users to upload TXT or PDF documents and ask questions about their content.

The system uses:

- FastAPI for the API
- Sentence Transformers for local embeddings
- Qdrant for vector storage and similarity search
- Groq with Llama 3.3 70B for answer generation
- Python for the backend
- Pytest for testing

## Features

- Upload TXT and PDF documents
- Split documents into smaller chunks
- Generate embeddings using Sentence Transformers locally
- Store document chunks and embeddings in Qdrant
- Retrieve the top 3 relevant chunks for each question
- Generate answers using Groq and Llama 3.3 70B
- Support multi-turn conversations
- Keep the last 6 conversation turns
- Return document sources with answers
- Answer "I don't know." when the information is not found in the document
- Query caching using session ID and query hash
- Streaming chat responses
- Automated tests using Pytest

## Project Structure

```text
document-qa-chatbot/
│
├── main.py
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── ingestion.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── llm.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
