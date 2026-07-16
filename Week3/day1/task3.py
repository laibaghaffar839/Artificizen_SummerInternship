from task1 import client

prompt = "Summarise what a transformer model does in 3 sentences."

print("Temperature = 0\n")
for i in range(3):
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user","content": prompt
        }
    ],
    temperature=0
    )

    print(f"Response {i+1}")
    print(response.choices[0].message.content)
    print("-"*50)

print("\nTemperature = 1.0\n")

for i in range(3):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=1.0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print(f"Response {i+1}")
    print(response.choices[0].message.content)
    print("-"*50)

# One line observation

# temperature=0 produced more consistent, almost same and similar responses, 
# while temperature=1.0 generated more varied and creative responses due to increased randomness.