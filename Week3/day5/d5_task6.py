from groq_function import ask
# Updated Ragas Imports
from ragas import evaluate, SingleTurnSample, EvaluationDataset
from ragas.metrics import Faithfulness, AnswerRelevancy

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
        "question": "What is the main purpose of the article?"
    },

    {
        "question": "Why is wheat important for Pakistan?"
    },

    {
        "question": "What effect did the support price policy have on wheat production and farmers' yield?"
    },

    {
        "question": "What methods were used to estimate the supply response of wheat?"
    },

    {
        "question": "What are some problems caused by agricultural policies in Pakistan?"
    }
]


# Store evaluation results
results = []

for i, item in enumerate(evaluation_data, start=1):

    question = item["question"]

    print(f"\nProcessing Question {i}...")
    print(question)

    # Retrieve relevant chunks
    retrieved_chunks = retrieve(question,collection,top_k=3)

    # Build prompt
    prompt = build_prompt(question,retrieved_chunks)

    # Generate answer
    answer = ask(prompt)

    # Get retrieved context
    context = []

    for chunk in retrieved_chunks:
        context.append(chunk["text"])

    results.append({

        "user_input": question,

        "response": answer,

        "retrieved_contexts": context

    })


print("\n")
print("=" * 60)
print("RAG ANSWERS")
print("=" * 60)

for i, result in enumerate(results, start=1):

    print(f"\nQuestion {i}:")
    print(result["user_input"])

    print("\nAnswer:")
    print(result["response"])

    print("\nRetrieved Context:")

    for context in result["retrieved_contexts"]:

        print("-", context[:300])

    print("\n" + "-" * 60)

print("\nCreating Ragas evaluation dataset...")

# CREATE RAGAS DATASET
dataset = EvaluationDataset.from_list(results)

# CREATE RAGAS METRICS
faithfulness = Faithfulness()

answer_relevancy = AnswerRelevancy()

# RUN RAGAS EVALUATION
print("\nRunning Ragas evaluation...")

ragas_result = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy
    ]
)

# PRINT RAGAS RESULTS
print("\n")
print("=" * 60)
print("RAGAS EVALUATION RESULTS")
print("=" * 60)

print(ragas_result)

# CONVERT RESULTS TO DATAFRAME

df = ragas_result.to_pandas()


print("\n")
print("=" * 60)
print("SCORES FOR EACH QUESTION")
print("=" * 60)

print(
    df[
        [
            "user_input",
            "faithfulness",
            "answer_relevancy"
        ]
    ]
)

# FIND LOWEST SCORING QUESTION

df["average_score"] = (df["faithfulness"]+df["answer_relevancy"]) / 2


lowest_index = df["average_score"].idxmin()


lowest_question = df.loc[lowest_index,"user_input"]


lowest_faithfulness = df.loc[lowest_index,"faithfulness"]


lowest_relevancy = df.loc[lowest_index,"answer_relevancy"]

# PRINT LOWEST SCORE
print("\n")
print("=" * 60)
print("LOWEST SCORING QUESTION")
print("=" * 60)

print("Question:",lowest_question)

print("Faithfulness:",lowest_faithfulness)

print("Answer Relevancy:",lowest_relevancy)

print("Average Score:",df.loc[lowest_index,"average_score"])
print("\nReason:")

print(
    "This question received the lowest average score "
    "because the generated answer was either less grounded "
    "in the retrieved context or less relevant to the question."
)




