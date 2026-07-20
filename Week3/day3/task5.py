from main import model
from random_text import sentences
import numpy as np

# Cosine similarity function
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

embeddings=model.encode(sentences)



query="A puppy is moving outside in a garden"


query_embedding=model.encode(query)



scores=[]


for text,vector in zip(sentences,embeddings):

    score=cosine_similarity(query_embedding,vector)

    scores.append((text,score))


scores.sort(key=lambda x:x[1],reverse=True)


for item in scores[:5]:
    print(item)