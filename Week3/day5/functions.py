import pymupdf4llm

# Load TXT file

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Load PDF file

def load_pdf(file_path):
    text = pymupdf4llm.to_markdown(file_path)
    return text

# Chunk text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start = end - overlap

    return chunks