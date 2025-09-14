import os
from pinecone import Pinecone, ServerlessSpec

# Set API key
API_KEY = "pcsk_7MRab3_H6BQLHFaNiQqyZ6EVuxf8od6Y9xtM9Yq8LaCnY8YZkQuJTzCScFwaWsL2GN9pa6"  # Your API key

ENVIRONMENT = "us-east-1"  # Verify region in Pinecone dashboard

# Initialize Pinecone
try:
    pc = Pinecone(api_key=API_KEY)
except Exception as e:
    print(f"Failed to initialize Pinecone: {e}")
    exit(1)

# Create index if it doesn't exist
index_name = "vectorscan-faults"

try:
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # For OpenAI text-embedding-ada-002
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=ENVIRONMENT
            )
        )
        print(f"Pinecone index '{index_name}' created successfully.")
    else:
        print(f"Pinecone index '{index_name}' already exists.")
except Exception as e:
    print(f"Error managing index: {e}")
    exit(1)