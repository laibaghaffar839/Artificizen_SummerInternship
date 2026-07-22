#1.	Write a chunk_text(text, chunk_size=500, overlap=50) function that splits a long 
#string into overlapping chunks. Print the number of chunks produced from a 3,000-word document.


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks


# Create a 3,000-word document
document = "This is a sample word. " * 131

# Create chunks
chunks = chunk_text(document, chunk_size=500, overlap=50)

# Print length of document and number of chunks
print(f"Document length: {len(document)}")
print("Number of chunks:", len(chunks))

