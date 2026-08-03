from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL


# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


# System instruction for grounded answers
SYSTEM_PROMPT = """
You are a helpful document question-answering assistant.

Answer the user's question ONLY using the information provided
in the context.

If the answer is not present in the context, respond exactly:
"I don't know."

Do not use outside knowledge.
Do not make up or assume information.
"""


def generate_answer(query: str,context: str,history: list = None) -> str:
    """
    Generate an answer using Groq based only on retrieved context.
    """

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add previous conversation history
    messages.extend(history)

    # Add current user query with retrieved context
    user_message = f"""Context:{context} Question:{query}"""

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Call Groq
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0,
        max_tokens=512
    )

    return response.choices[0].message.content


def generate_answer_stream(query: str,context: str,history: list = None):
    """
    Generate a streaming answer using Groq.
    """

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add previous conversation history
    messages.extend(history)

    # Add current user query with retrieved context
    user_message = f"""Context:{context} Question:{query}"""

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Call Groq
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0,
        max_tokens=512,
        stream=True
    )

    # Yield each generated token
    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            yield content