# Multimodal AI-Powered Retail Workspace RAG Platform

## Industry

**E-commerce & Retail Intelligence**

---

## Problem Statement

Retail and e-commerce teams manage large amounts of business information scattered across different file formats, including supplier contracts, product catalogs, inventory spreadsheets, presentations, images, audio recordings, and promotional videos. Finding specific information manually across these files can be time-consuming and may lead to operational delays and loss of important context.

This platform unifies retail business information into a secure, room-based Retrieval-Augmented Generation (RAG) system. Users can create dedicated workspace rooms, upload multiple types of files, and ask questions in natural language. The system retrieves relevant information from uploaded files and generates grounded answers with source citations.

---

## Key Features

* Secure user registration and login using JWT authentication
* Bcrypt password hashing
* Room-based workspace management
* Multimodal file upload and processing
* Support for PDF, DOCX, CSV, PPTX, MD, TXT, PNG, JPG, MP3, WAV, and MP4 files
* Image text extraction using Tesseract OCR
* Audio transcription using Groq Whisper
* Video-to-text processing through audio extraction and Whisper
* Text chunking with overlapping segments
* Embeddings using `all-MiniLM-L6-v2`
* Semantic search using Qdrant
* RAG-based question answering using Groq Llama 3.3
* Persistent conversation history
* Source citations for generated answers
* PostgreSQL database for application data
* Protected API routes and user-specific access control

---

## Repository Directory Structure

```text
.
├── alembic/                  # Database migration scripts
│   ├── versions/             # Migration version histories
│   └── env.py                # Alembic environment configuration
│
├── db/                       # Database models and session management
│   ├── database.py           # SQLAlchemy database session and engine
│   └── models.py             # User, ChatRoom, UploadedFile, and ChatMessage models
│
├── routers/                  # FastAPI endpoint handlers
│   ├── auth.py               # Authentication endpoints
│   ├── chat.py               # Chat and history endpoints
│   ├── rooms.py              # Chat room management endpoints
│   └── upload.py             # File upload and ingestion endpoints
│
├── schemas/                  # Pydantic request and response schemas
│   ├── auth.py               # Authentication schemas
│   ├── chat.py               # Chat schemas
│   └── room.py               # Room schemas
│
├── services/                 # Core application logic
│   ├── ingestion/            # File extraction modules
│   │   ├── audio.py          # Audio transcription
│   │   ├── csv.py            # CSV parser
│   │   ├── docx.py           # DOCX parser
│   │   ├── image.py          # Image OCR extractor
│   │   ├── markdown.py       # Markdown parser
│   │   ├── pdf.py            # PDF parser
│   │   ├── pptx.py           # PowerPoint parser
│   │   ├── txt.py            # Text file parser
│   │   └── video.py          # Video audio extraction
│   │
│   ├── auth.py               # JWT and password hashing
│   ├── chunker.py            # Text chunking logic
│   ├── embedder.py           # Embedding generation
│   ├── groq_client.py        # Groq LLM client
│   ├── qdrant.py             # Qdrant vector storage
│   └── rag.py                # RAG retrieval and generation
│
├── uploads/                  # Local uploaded file storage
├── .env                      # Environment variables
├── .gitignore                # Git exclusion rules
├── alembic.ini               # Alembic configuration
├── config.py                 # Application configuration
├── main.py                   # FastAPI application entry point
├── streamlit_app.py          # Streamlit frontend
└── requirement.txt           # to manage all dependencies 
└── Readme.md.py 
```

---

## Technologies Used

| Component           | Technology              |
| ------------------- | ----------------------- |
| Frontend            | Streamlit               |
| Backend             | FastAPI                 |
| Database            | PostgreSQL              |
| ORM                 | SQLAlchemy              |
| Authentication      | JWT + Bcrypt            |
| Vector Database     | Qdrant                  |
| Embeddings          | Sentence Transformers   |
| Embedding Model     | `all-MiniLM-L6-v2`      |
| LLM                 | Groq Llama 3.3          |
| Audio Transcription | Groq Whisper            |
| Image OCR           | Tesseract + Pytesseract |
| PDF Processing      | PyMuPDF4LLM             |
| DOCX Processing     | python-docx             |
| CSV Processing      | Pandas                  |
| PPTX Processing     | python-pptx             |
| Video Processing    | MoviePy                 |
| Database Migrations | Alembic                 |

---

## System Requirements and Prerequisites

### Tesseract OCR

Image text extraction uses Tesseract OCR through Pytesseract.

#### macOS using MacPorts

```bash
sudo port selfupdate
sudo port install tesseract
```

#### macOS using Homebrew

```bash
brew install tesseract
```

#### Ubuntu / Linux

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr -y
```

---

## Installation Guide

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

For macOS or Linux:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## requirements.txt (IMPORTANT)

This project uses a `requirements.txt` file to manage all dependencies and ensure consistent environment setup across different systems.

### Generate requirements.txt

After installing all dependencies in your environment, generate the file using:

```bash
pip freeze > requirements.txt
```

### Install from requirements.txt

On any new system, install all dependencies using:

```bash
pip install -r requirements.txt
```

### Why requirements.txt is important

* Ensures same package versions across all environments
* Prevents compatibility issues between development and production
* Makes project deployment easier
* Required for reproducibility in AI/ML pipelines

### Recommended practice

Always update `requirements.txt` after installing new packages:

```bash
pip install new-package
pip freeze > requirements.txt
```

---

## PostgreSQL Database Setup

The application uses PostgreSQL with SQLAlchemy ORM for persistent data storage.

Make sure PostgreSQL is installed and running on your system.

Create a PostgreSQL database for the project and configure the database connection in the `.env` file.

Example:

```env
DATABASE_URL="postgresql://username:password@localhost:5433/database_name"  # you can use your port like 5432
```

Replace the following values according to your PostgreSQL configuration:

* `username` — PostgreSQL username
* `password` — PostgreSQL password
* `5433` — PostgreSQL port
* `database_name` — Project database name

The database stores:

* User accounts
* Chat rooms
* Chat messages
* Uploaded file metadata

---

## Environment Variables

Create a `.env` file in the root directory of the project.

```env
# Application Settings
SECRET_KEY="your-super-secret-jwt-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Groq API Key
GROQ_API_KEY="gsk_your_groq_api_key_here"

# PostgreSQL Database
DATABASE_URL="postgresql://username:password@localhost:5433/database_name"
```

Never commit your `.env` file or API keys to GitHub. Make sure `.env` is included in `.gitignore`.

---

## Running the Application

The application requires two running processes:

1. FastAPI backend
2. Streamlit frontend

### Step 1: Start FastAPI Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Docs:

```text
http://127.0.0.1:8000/docs
```

### Step 2: Start Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

## System Workflow

```text
User Registration / Login
          ↓
      JWT Token
          ↓
    Create Chat Room
          ↓
      Upload Files
          ↓
   File-Type Extraction
          ↓
      Text Chunking
          ↓
    Generate Embeddings
          ↓
     Store in Qdrant
          ↓
      User Question
          ↓
   Query Embedding
          ↓
  Retrieve Relevant Chunks
          ↓
 Combine Context + Chat History
          ↓
      Groq LLM
          ↓
    Grounded Answer
          ↓
   Answer + Source Citations
```

---

## Supported File Formats

| File Type | Processing Method      |
| --------- | ---------------------- |
| PDF       | PyMuPDF4LLM            |
| DOCX      | python-docx            |
| CSV       | Pandas                 |
| PNG / JPG | Tesseract OCR          |
| MP3 / WAV | Groq Whisper           |
| MP4       | MoviePy + Groq Whisper |
| PPTX      | python-pptx            |
| MD        | Python file I/O        |
| TXT       | Python file I/O        |

---

## Multimodal Ingestion Pipeline

* PDF → Markdown extraction
* DOCX → structured text extraction
* CSV → row-wise conversion
* Images → OCR text extraction
* Audio → Whisper transcription
* Video → audio extraction + transcription
* PPTX → slide-wise text extraction
* TXT/MD → direct reading

---

## RAG Pipeline

Chunking:

```text
Chunk Size: 500
Overlap: 50
```

Embedding Model:

```text
all-MiniLM-L6-v2 (384 dimensions)
```

Flow:

```text
Extract → Chunk → Embed → Store → Retrieve → Augment → Generate → Cite
```

---

## Authentication and Security

* JWT-based authentication
* Bcrypt password hashing
* Protected API routes
* User-specific data isolation

---

## Testing

```bash
pytest
```

---

## Project Summary

This project demonstrates a full-stack **Multimodal RAG system** combining FastAPI, Streamlit, PostgreSQL, Qdrant, and Groq LLMs to enable intelligent document understanding for retail and e-commerce workflows.

