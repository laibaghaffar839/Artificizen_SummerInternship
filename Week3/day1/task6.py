from task1 import client
import time

prompt = "Summarise what a transformer model does in 3 sentences."

models = ["llama-3.3-70b-versatile","llama-3.1-8b-instant"]

for model in models:

    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    end = time.time()

    print("="*60)
    print("Model:", model)
    print("="*60)
    print("\nResponse:")
    print(response.choices[0].message.content)

    print("\nTotal Tokens:",response.usage.total_tokens)

    print("Latency:",round(end-start, 2),"seconds\n")