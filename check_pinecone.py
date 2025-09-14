import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("vectorscan-faults")

# Get index stats
stats = index.describe_index_stats()
print(stats)