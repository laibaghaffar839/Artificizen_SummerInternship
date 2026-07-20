# Embeddings & Semantic Search

## Overview

This project is a practice of embeddings, semantic search, and vector databases using Python. It demonstrates how text can be converted into vector embeddings, compared based on meaning, and stored in vector databases for efficient retrieval.

---

## What I Learned

- Understanding text embeddings
- Using the `all-MiniLM-L6-v2` Sentence Transformer model
- Generating embeddings for text
- Measuring similarity using cosine similarity
- Performing semantic search
- Working with vector databases
- Creating and querying ChromaDB collections
- Creating and querying Qdrant collections
- Storing metadata with vector embeddings
- Filtering search results using metadata
- Batch embedding and storing multiple documents
- Building reusable utility functions for future RAG applications

---

## Technologies Used

- Python
- Sentence Transformers
- NumPy
- ChromaDB
- Qdrant

---

## Project Files

- `main.py`
- `task1.py`
- `task2.py`
- `task3.py`
- `task4.py`
- `task5.py`
- `task6.py`

---

## Key Concepts

### Embeddings
Embeddings convert text into numerical vectors while preserving the semantic meaning of the text.

### Cosine Similarity
Cosine similarity measures how similar two vectors are. It is commonly used to compare embeddings.

### Semantic Search
Semantic search finds documents based on their meaning rather than exact keyword matches.

### ChromaDB
ChromaDB is a vector database used to store embeddings and perform semantic searches.

### Qdrant
Qdrant is a vector database that stores embeddings along with metadata and supports filtered searches.

### Metadata
Metadata provides additional information about stored documents, such as their source or category.

### Batch Embedding
Batch embedding allows multiple documents to be converted into embeddings and stored efficiently in a single operation.

### RAG Preparation
The reusable embedding and storage utility created in this project can be used later for building Retrieval-Augmented Generation (RAG) applications.

---

## Conclusion

This project helped me understand the complete workflow of semantic search, from generating embeddings to storing and retrieving vectors using ChromaDB and Qdrant. It also provided a strong foundation for building Retrieval-Augmented Generation (RAG) systems in future projects.
