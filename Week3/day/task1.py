from groq import Groq
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key= api_key
)