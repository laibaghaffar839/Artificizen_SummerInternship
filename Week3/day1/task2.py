from task1 import client

# Call Groq API
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Summarise what a transformer model does in 3 sentences."
        }
    ]
)


# Print AI response
print(response.choices[0].message.content)
print(response.usage)