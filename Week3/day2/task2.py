from main import ask

messages = [
    "The delivery was late and my package arrived damaged.",
    "How can I reset my password?",
    "Your customer service was amazing!",
    "I want to know your refund policy.",
    "The product quality is excellent."
]

for message in messages:
    prompt = f"""
Here are some examples:

Example 1:
Customer message: "My order arrived two days late and I am disappointed."
Category: Complaint

Example 2:
Customer message: "How can I change my account password?"
Category: Question

Example 3:
Customer message: "Your delivery service was excellent. Thank you!"
Category: Compliment


Now classify this customer message:

Customer message: "{message}"

Return only the category name."""
    result = ask(prompt)
    print(f"Customer Message:{message}")
    print(f"Category:{result}")
    print("-"*50)
    print("\n")


# Observation:
# Zero-shot Accuracy: 80%
# Few-shot Accuracy: 100%
# Few-shot prompting produced more consistent classifications because examples 
# helped the model understand the expected labels and format.

