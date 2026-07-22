# 4.Write a build_prompt(query, chunks) function that inserts the retrieved chunks as numbered context items and appends: “Answer using only the context above. If the answer is not in the context, say: I don’t know.”

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


# Test
chunks = retrieve(
    "What is artificial intelligence?",
    "Agriculture Article",
    top_k=3
)

prompt = build_prompt(
    "What is artificial intelligence?",
    chunks
)

print(prompt)


