from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

# Load embedding model once
model = SentenceTransformer(EMBEDDING_MODEL)

# Generate embeddings for multiple texts
def generate_embeddings(texts: list[str]):

    # Convert a list of text chunks into embeddings.
    embeddings = model.encode(texts)
    return embeddings

# Generate embedding for a single text
def generate_query_embedding(text: str):

    # Convert a single query into an embedding.
    embedding = model.encode([text])
    return embedding[0]
