# Day 4 - RAG (Retrieval-Augmented Generation)

## About

In this project, I learned the basic RAG pipeline. RAG helps an AI model answer questions using information from a document.

## What I Learned

- Loading text from PDF and TXT files
- Splitting documents into smaller chunks
- Creating embeddings using Sentence Transformers
- Storing embeddings in Qdrant
- Adding metadata such as source filename and chunk index
- Retrieving the most relevant chunks from Qdrant
- Building a prompt using retrieved context
- Using Groq to generate answers
- Comparing RAG answers with raw LLM answers
- Understanding how RAG helps reduce hallucinations

## RAG Pipeline

Load Document → Chunk Text → Create Embeddings → Store in Qdrant → Retrieve Relevant Chunks → Build Prompt → Generate Answer

## Project Files

- `functions.py` - Contains functions for loading PDF/TXT files and creating text chunks.
- `model.py` - Contains embedding, Qdrant storage, retrieval, and prompt functions.
- `groq_function.py` - Contains the Groq API `ask()` function.
- `task1.py` - Practice for text chunking.
- `task2.py` - Loads a document, chunks it, embeds the chunks, and stores them in Qdrant.
- `task3.py` - Retrieves the most relevant chunks from Qdrant.
- `task4.py` - Builds a prompt using retrieved context.
- `task5.py` - Connects retrieval, prompt building, and Groq to answer questions.
- `task6.py` - Compares RAG answers with raw Groq answers to test hallucination.
- `article 2.pdf` - The document used for the RAG pipeline.
- `.env` - Stores the Groq API key securely.

## Conclusion

This project helped me understand how RAG connects documents with LLMs. Instead of answering only from its own knowledge, the model uses relevant information retrieved from the document.
