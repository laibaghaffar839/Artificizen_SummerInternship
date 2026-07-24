from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Read Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model configuration
GROQ_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Qdrant configuration
COLLECTION_NAME = "documents"

# Chunking configuration
chunk_size = 500
overlap = 50