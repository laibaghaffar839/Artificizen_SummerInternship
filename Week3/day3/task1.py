from main import model
import numpy as np

sentences = [
    "A dog is chasing a ball",
    "A puppy is playing with a toy",
    "The cat is sleeping on the sofa",
    "A man is running in the park",
    "Dogs love playing outdoors",
    "A car is driving on the road"
]

# Create embeddings
embeddings = model.encode(sentences)

# Cosine similarity function
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


results = []

# Compare first sentence with others
query_embedding = embeddings[0]

for i in range(1, len(sentences)):
    score = cosine_similarity(query_embedding, embeddings[i])
    results.append((sentences[i], score))


# Sort highest similarity first
results.sort(key=lambda x: x[1], reverse=True)


print("Similarity Ranking:\n")

for text, score in results:
    print(f"{text} = {score:.4f}")