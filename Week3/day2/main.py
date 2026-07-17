from groq import Groq
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key= api_key)

# ask function
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

