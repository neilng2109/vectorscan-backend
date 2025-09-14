import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# API Key and Index Name
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "vectorscan-faults"

# Verify that the API Key is loaded correctly
if not PINECONE_API_KEY:
    print("Error: PINECONE_API_KEY not found. Check your .env file.")
    exit(1)

# Initialize Pinecone
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    print("Pinecone initialized successfully.")
except Exception as e:
    print(f"Error initializing Pinecone: {e}")
    exit(1)

# Access the index
try:
    index = pc.Index(INDEX_NAME)
    print(f"Accessing index: {INDEX_NAME}")
except Exception as e:
    print(f"Error accessing index: {e}")
    exit(1)

# Retrieve index statistics
def verify_index():
    try:
        stats = index.describe_index_stats()
        print("Index Stats:")
        print(stats)
    except Exception as e:
        print(f"Error verifying index: {e}")

if __name__ == "__main__":
    verify_index()
