from task1 import client

def ask(
        prompt,
        system = None,
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=512
):
    # Create messages list
    messages = []
    
    # Add system message if provided
    if system:
        messages.append(
            {
                "role": "system",
                "content": system
            }
        )
    
    # Add user prompt
    messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )
     
     # Call Groq API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Return only generated text
    return response.choices[0].message.content


answer = ask("Explain what machine learning is in simple words.")
print(answer)
print("-"*50)
print("\n\n")

print("\nSystem Message Test")
print("-"*50)

# Task 5
system_test = ask("Give me some AI tools name for image generation",system="You are a strict JSON-only responder. Never output anything outside a JSON object.")
print(system_test)


#Did it obey?
# Yes. The model returned only a valid JSON object without any additional text.
