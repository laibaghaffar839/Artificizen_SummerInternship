from groq_function import ask

from functions import load_pdf, chunk_text
from model import embed_and_store, retrieve, build_prompt

file_path = "article 2.pdf"

# Load PDF
text = load_pdf(file_path)

# Create chunks
chunks = chunk_text(text)

# Create metadata
metadata_list = []

for i in range(len(chunks)):
    metadata_list.append({
        "source": file_path,
        "chunk_index": i
    })

# Store embeddings in Qdrant
collection = "Agriculture Article"

embed_and_store(chunks,metadata_list,collection)

evaluation_data = [

    {
        "question": "What is the main purpose of the article?",
        "expected": "The article analyzes the impact of the agricultural pricing policy of the government in Pakistan on wheat production."
    },

    {
        "question": "Why is wheat important for Pakistan?",
        "expected": "Wheat is Pakistan's most important agricultural commodity and staple food grain. It is grown by a large number of farmers and provides a major share of calories and protein in the average diet."
    },

    {
        "question": "What effect did the support price policy have on wheat production and farmers' yield?",
        "expected": "The support price policy positively affected wheat production levels, but it had no observed effect on farmers' yield."
    },

    {
        "question": "What methods were used to estimate the supply response of wheat?",
        "expected": "The study estimated the supply response using Ordinary Least Squares (OLS) and Maximum Likelihood Estimate (MLE) methods."
    },

    {
        "question": "What are some problems caused by agricultural policies in Pakistan?",
        "expected": "The policies caused welfare and efficiency losses, harmed producers, and included inconsistent government interventions and input subsidies that were biased toward large farmers."
    }
]

# Store evaluation results
results = []

correct_count = 0


# Evaluate each question
for item in evaluation_data:

    question = item["question"]
    expected = item["expected"]

    # Retrieve relevant chunks
    retrieved_chunks = retrieve(question,collection,top_k=3)

    # Build prompt
    prompt = build_prompt(question,retrieved_chunks)

    # Generate answer
    answer = ask(prompt)

    print("\nQuestion:", question)
    print("Expected Answer:", expected)
    print("RAG Answer:", answer)

    # Manual evaluation
    score = input("Enter score (Correct / Partially Correct / Wrong): ")

     # Count correct answers
    if score.lower() == "correct":
        correct_count += 1

    results.append({
        "question": question,
        "expected_answer": expected,
        "rag_answer": answer,
        "score": score
    })


# Calculate accuracy
accuracy = (correct_count / len(evaluation_data)) * 100

print("\nEvaluation Results\n")

for result in results:

    print("\nQuestion:", result["question"])
    print("Score:", result["score"])


print("\nAccuracy:", accuracy, "%")
