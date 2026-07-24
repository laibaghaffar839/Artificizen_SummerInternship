from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

from app.config import COLLECTION_NAME

# Create Qdrant client
client = QdrantClient(":memory:")

# Create collection if it does not exist
def create_collection():
    collections = client.get_collections().collections

    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

# Store document chunks and their embeddings
def store_chunks(chunks: list[str],embeddings,source_filename: str):
    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload={
                "text": chunk,
                "source": source_filename,
                "chunk_index": index
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


# Search for the most relevant chunks
def search_similar_chunks(query_embedding,top_k: int = 3):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=top_k
    ).points

    return results