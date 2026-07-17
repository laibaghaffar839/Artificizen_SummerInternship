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
Classify this customer message as one of:
Complaint, Question, or Compliment.
Message:{message}
only return category name"""
    result = ask(prompt, temperature=0)
    print(message)
    print(f"Classification:{result}")
    print("-"*50)

