# 3.Write a retrieve(query, collection, top_k=3) function that embeds the query with sentence-transformers and returns the top-k chunks from Qdrant.

from model import retrieve
from functions import load_pdf, load_txt, chunk_text
from model import embed_and_store
from pathlib import Path


# Load document

file_path = "article 2.pdf"

if file_path.endswith(".txt"):
    text = load_txt(file_path)

elif file_path.endswith(".pdf"):
    text = load_pdf(file_path)

else:
    raise ValueError("Only .txt and .pdf files are supported")


# Create chunks
chunks = chunk_text(text)

# Create metadata
metadata_list = []

for i in range(len(chunks)):

    metadata = {
        "source": Path(file_path).name,
        "chunk_index": i
    }

    metadata_list.append(metadata)



print("Number of chunks:", len(chunks))




embed_and_store(chunks, metadata_list,"Agriculture Article")

print("Chunks stored in Qdrant")

# retrieve
results = retrieve(
    "Is there any concept of regression used here?",
    "Agriculture Article",
    top_k=3
)

for result in results:
    print(result)