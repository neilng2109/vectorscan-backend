import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv("C:/Users/neilg/vectorscan/venv/.env")

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Define index name and specifications
index_name = "vectorscan-faults"
dimension = 1536  # Matches text-embedding-ada-002
metric = "cosine"

# Check if index already exists
if index_name not in pc.list_indexes().names():
    # Create the index
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric=metric,
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"Created index: {index_name}")
else:
    print(f"Index {index_name} already exists.")

# Verify index creation
print(pc.describe_index(index_name))