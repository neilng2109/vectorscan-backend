import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("C:/Users/neilg/vectorscan/venv/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(f"OpenAI API Key exists: {bool(OPENAI_API_KEY)}")
print(f"OpenAI API Key starts with: {OPENAI_API_KEY[:10] if OPENAI_API_KEY else 'None'}...")

try:
    from openai import OpenAI
    print("OpenAI import successful")
    
    # Test client initialization
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("OpenAI client created successfully")
    
    # Test embeddings
    response = client.embeddings.create(
        input="test fault",
        model="text-embedding-ada-002"
    )
    print(f"Embeddings test successful: {len(response.data[0].embedding)} dimensions")
    
    # Test chat completion
    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Test message"}],
        max_tokens=10
    )
    print(f"Chat completion test successful: {chat_response.choices[0].message.content}")
    
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e)}")
