from main import model
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)



client=QdrantClient(":memory:")


client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)


texts=[
"Python programming guide",
"Machine learning manual",
"Cooking recipes book",
"AI engineering notes",
"Database documentation"
]


sources=[
"manual",
"manual",
"book",
"manual",
"docs"
]


vectors=model.encode(texts)


points=[]


for i,(text,source,vector) in enumerate(
    zip(texts,sources,vectors)
):

    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={
                "text":text,
                "source":source
            }
        )
    )


client.upsert(
    collection_name="docs",
    points=points
)



query="Artificial intelligence learning"


query_vector=model.encode(query)


results = client.query_points(
    collection_name="docs",
    query=query_vector.tolist(),
    limit=2,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="source",
                match=MatchValue(value="manual")
            )
        ]
    )
)


for point in results.points:
    print(point.payload)
    print(point.score)