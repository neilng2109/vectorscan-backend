import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_embedding(text):
    """
    Generate embedding using the latest OpenAI API structure.
    """
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response['data'][0]['embedding']
        print(f"Embedding generated successfully for: {text}")
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

if __name__ == "__main__":
    # Test with a sample fault description
    test_text = "Cooling pump overheating due to coolant leak"
    embedding = generate_embedding(test_text)
    if embedding:
        print(f"Generated embedding length: {len(embedding)}")
        print(f"Sample of embedding data: {embedding[:10]}")
