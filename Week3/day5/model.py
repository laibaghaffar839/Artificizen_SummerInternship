from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create in-memory Qdrant database
client = QdrantClient(":memory:")


def embed_and_store(texts, metadata_list, collection_name = "documents"):
    """
    Batch embed texts and store them in Qdrant with metadata.

    Parameters:
        texts (list): List of strings
        metadata_list (list): List of metadata dictionaries
        collection (str): Qdrant collection name
    """
    # Create collection
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,  # MiniLM-L6-v2 vector dimension
                distance=Distance.COSINE
            )
        )

    # Create embeddings
    embeddings = model.encode(texts)

    # Create Qdrant points
    points = []

    for i, (text, metadata, embedding) in enumerate(
        zip(texts, metadata_list, embeddings)
    ):
        point = PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={
                "text": text,
                **metadata
            }
        )

        points.append(point)

    # Store in Qdrant
    client.upsert(
        collection_name=collection_name,
        points=points
    )

    print(f"{len(points)} documents stored successfully!")

# retrieve query
def retrieve(query, collection_name, top_k=3):

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name= collection_name,
        query= query_embedding,
        limit= top_k
    ).points

    retrieved_chunks = []

    for result in results:

        retrieved_chunks.append({
            "text": result.payload["text"],
            "source": result.payload["source"],
            "chunk_index": result.payload["chunk_index"],
            "score": result.score
        })

    return retrieved_chunks


# build prompt

def build_prompt(query, chunks):

    context = ""

    for i, chunk in enumerate(chunks, start=1):

        context += f"""
Context {i}:
{chunk['text']}
"""

    prompt = f"""
You are a helpful assistant.

Use only the provided context to answer the question.

{context}

Question:
{query}

Answer using only the context above.
If the answer is not in the context, say: I don't know.
"""

    return prompt


