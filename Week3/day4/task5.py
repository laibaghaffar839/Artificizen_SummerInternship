# 5.Wire everything together: retrieve() → build_prompt() → ask() (using Groq). Ask three questions — two with answers in the document and one without. Verify the model says “I don’t know” for the third.

from model import embed_and_store, retrieve , build_prompt
from functions import load_pdf, load_txt, chunk_text
from pathlib import Path
from groq_function import ask


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

# Emmbed
embed_and_store(chunks, metadata_list,"Agriculture Article")


# testing function
def rag_answer(query):

    # Step 1: Retrieve relevant chunks
    chunks = retrieve(
        query,
        "Agriculture Article",
        top_k=3
    )

    # Step 2: Build prompt
    prompt = build_prompt(
        query,
        chunks
    )

    # Step 3: Send prompt to Groq
    answer = ask(prompt)

    return answer

# Testing
questions = [
    "What is agriculture?",
    "Why regression used in this article?",
    "Who invented the first computer?"
]


for question in questions:

    print("\nQuestion:", question)

    answer = rag_answer(question)

    print("Answer:", answer)