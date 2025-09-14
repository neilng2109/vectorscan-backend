import pinecone
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")
print("Initializing Pinecone...")
pc = pinecone.Pinecone(api_key=api_key)
print("Listing indexes...")
print(pc.list_indexes())