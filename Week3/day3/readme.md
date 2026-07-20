# Embeddings & Semantic Search Practice

## Overview

In this practice, I learned how text embeddings work and how semantic search finds documents based on meaning instead of exact words. I also learned how to use ChromaDB and Qdrant to store and search vector embeddings.

---

## Topics Learned

- What an embedding is
- How Sentence Transformers create embeddings
- Cosine similarity
- Semantic search
- Vector databases
- ChromaDB (in-memory)
- Qdrant (in-memory)
- Metadata and payloads
- Filtering search results
- Batch embedding and storing data

---

## Tools Used

- Python
- sentence-transformers
- NumPy
- ChromaDB
- Qdrant

---

# Question 1

**Task:**
Embed six sentences and calculate cosine similarity between them.

**What I learned:**
- Generate embeddings using `all-MiniLM-L6-v2`
- Compare sentence similarity
- Rank results from highest to lowest similarity

**Output:**

![alt text](task1.png)

---

# Question 2

**Task:**
Create a `semantic_search()` function to find the top 3 most similar documents.

**What I learned:**
- Embed both query and documents
- Calculate cosine similarity
- Return the most relevant documents

**Output:**

![alt text](task2.png)

---

# Question 3

**Task:**
Store documents in ChromaDB and perform semantic search.

**What I learned:**
- Create an in-memory ChromaDB collection
- Store embeddings
- Query using natural language

**Output:**

![alt text](task3.png)

---

# Question 4

**Task:**
Store documents in Qdrant and filter results using metadata.

**What I learned:**
- Create a Qdrant collection
- Store vectors with payloads
- Filter documents using the `source` field

**Output:**

![alt text](task4.png)

---

# Question 5

**Task:**
Test semantic search with different words but similar meaning.

**What I learned:**
- Semantic search understands meaning, not just exact words.
- Similar sentences can be matched even if they use different vocabulary.

**Output:**

![alt text](task5.png)

---

# Question 6

**Task:**
Create an `embed_and_store()` utility function.

**What I learned:**
- Batch embed multiple documents
- Store vectors with metadata
- Reuse the function for future RAG projects

**Output:**

![alt text](task6.png)

---

## Conclusion

This practice helped me understand how embeddings convert text into vectors and how semantic search retrieves the most relevant documents. I also learned to use ChromaDB and Qdrant for vector storage, metadata filtering, and document retrieval. The `embed_and_store()` function will be useful when building a Retrieval-Augmented Generation (RAG) pipeline.