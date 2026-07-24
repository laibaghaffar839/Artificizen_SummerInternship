from pathlib import Path
import pymupdf4llm

# Load TXT file
def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Load PDF file
def load_pdf(file_path: str) -> str:
    text = pymupdf4llm.to_markdown(file_path)
    return text

# Load TXT or PDF document
def load_document(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()
    if extension == ".txt":
        return load_txt(file_path)

    elif extension == ".pdf":
        return load_pdf(file_path)

    else:
        raise ValueError("Unsupported file type. Only .txt and .pdf files are allowed.")

# Chunk text
def chunk_text(text: str,chunk_size: int = 500,overlap: int = 50) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start = end - overlap

    return chunks
