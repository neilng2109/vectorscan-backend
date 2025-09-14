import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

if openai_key:
    print("OpenAI Key Loaded Successfully")
else:
    print("Error: OpenAI Key not found.")
