from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create in-memory Qdrant database
client = QdrantClient(":memory:")

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,  # Embedding size of all-MiniLM-L6-v2
        distance=Distance.COSINE
    )
)

# Get collection object (just the collection name)
collection = "documents"


def embed_and_store(texts, metadata_list, collection):
    """
    Batch embed texts and store them in Qdrant with metadata.

    Parameters:
        texts (list): List of strings
        metadata_list (list): List of metadata dictionaries
        collection (str): Qdrant collection name
    """

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
        collection_name=collection,
        points=points
    )

    print(f"{len(points)} documents stored successfully!")


#  Example  

texts = [
    "FastAPI is used to build APIs.",
    "Python is a popular programming language.",
    "Machine Learning finds patterns in data.",
    "Qdrant is a vector database.",
    "RAG combines retrieval with language models."
]

metadata = [
    {"source": "notes", "topic": "FastAPI"},
    {"source": "manual", "topic": "Python"},
    {"source": "manual", "topic": "Machine Learning"},
    {"source": "documentation", "topic": "Qdrant"},
    {"source": "tutorial", "topic": "RAG"}
]

embed_and_store(texts, metadata, collection)


#  Verify  

results = client.scroll(
    collection_name=collection,
    limit=10,
    with_payload=True,
    with_vectors=False
)

print("\nStored Documents:\n")

for point in results[0]:
    print(point.payload)