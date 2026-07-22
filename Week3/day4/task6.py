# 6.Test hallucination: run the same question WITHOUT the RAG context (raw Groq call only). Compare the answer to the RAG answer. Write a short observation on which is more grounded and why.

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

question = "Who invented the first computer?"

rag_result = rag_answer(question)

print("RAG Answer:")
print(rag_result)

raw_result = ask(question)

print("\nRaw Groq Answer:")
print(raw_result)

# observation

# The RAG answer is more grounded because the model receives relevant information retrieved 
# from the document and is instructed to use only that context. If the answer is not available 
# in the document, the model should say "I don't know." The raw Groq answer does not have access 
# to the document, so it may use its general knowledge or generate an unsupported answer. Therefore,
# RAG helps reduce hallucination by grounding the model's response in retrieved information.