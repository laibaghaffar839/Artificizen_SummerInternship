import chromadb
from main import model

client = chromadb.Client()


collection = client.create_collection(
    name="knowledge"
)


documents=[
"Python is used for artificial intelligence",
"Machine learning learns patterns from data",
"Deep learning uses neural networks",
"Cars use engines for movement",
"Dogs are common household pets",
"Cats like climbing trees",
"The earth revolves around the sun",
"Water freezes at zero degrees",
"Plants need sunlight to grow",
"Computers process information"
]


embeddings=model.encode(documents)


collection.add(
    documents=documents,
    embeddings=embeddings.tolist(),
    ids=[str(i) for i in range(10)]
)


query="How does AI learn from information?"


query_embedding=model.encode(query)


result=collection.query(
    query_embeddings= query_embedding.tolist(),
    n_results=2
    
   
)


print(result["documents"])