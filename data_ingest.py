import os
import pandas as pd
from dotenv import load_dotenv
import openai
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec

print("Starting script...")

# Load environment variables
try:
    print("Loading .env file...")
    load_dotenv("C:/Users/neilg/vectorscan/venv/.env")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    print(f"PINECONE_API_KEY: {'Set' if PINECONE_API_KEY else 'Not set'}")
    print(f"OPENAI_API_KEY: {'Set' if OPENAI_API_KEY else 'Not set'}")
    if not PINECONE_API_KEY or not OPENAI_API_KEY:
        raise ValueError("Missing API keys in .env file")
except Exception as e:
    print(f"Error loading environment variables: {e}")
    exit(1)

INDEX_NAME = "vectorscan-faults"
NAMESPACE = ""  # Default namespace; try "faults" if this fails

# Initialize Pinecone
try:
    print("Initializing Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    print("Checking index...")
    if INDEX_NAME not in pc.list_indexes().names():
        print(f"Creating index: {INDEX_NAME}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    index = pc.Index(INDEX_NAME)
    stats = index.describe_index_stats()
    print(f"Index stats before ingestion: {stats}")
except Exception as e:
    print(f"Error initializing Pinecone: {e}")
    exit(1)

# Initialize OpenAI client
try:
    print("Initializing OpenAI client...")
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"Error initializing OpenAI: {e}")
    exit(1)

def generate_embedding(text):
    print(f"Generating embedding for text: {text[:50]}...")
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response.data[0].embedding
        print(f"Embedding length: {len(embedding)}")
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def ingest_data(file_path):
    print(f"Loading CSV file: {file_path}")
    try:
        data = pd.read_csv(file_path)
        print(f"Loaded {len(data)} records from {file_path}")
        if data.empty:
            print("CSV file is empty")
            return

        # Handle NaN values
        data["Fault Description"] = data["Fault Description"].fillna("Unknown Fault")
        data["Equipment Affected"] = data["Equipment Affected"].fillna("Unknown Equipment")
        data["Cause (If known)"] = data["Cause (If known)"].fillna("Unknown Cause")
        data["Resolution Action"] = data["Resolution Action"].fillna("Not specified")

        # Validate IDs
        print(f"Missing IDs: {data['Fault Entry ID'].isnull().sum()}")
        print(f"Duplicate IDs: {data['Fault Entry ID'].duplicated().sum()}")

        vectors = []
        for _, row in tqdm(data.iterrows(), total=len(data), desc="Ingesting data"):
            embedding = generate_embedding(row["Fault Description"])
            if embedding is None:
                continue
            fault_id = str(row["Fault Entry ID"])
            if not fault_id or fault_id == "nan":
                print(f"Skipping invalid ID for row: {row}")
                continue
            metadata = {
                "fault": str(row["Fault Description"]),
                "equipment": str(row["Equipment Affected"]),
                "cause": str(row["Cause (If known)"]),
                "resolution": str(row["Resolution Action"])
            }
            vectors.append((fault_id, embedding, metadata))

        if not vectors:
            print("No valid vectors generated")
            return

        print(f"Sample vector: ID={vectors[0][0]}, Embedding length={len(vectors[0][1])}, Metadata={vectors[0][2]}")
        print(f"Upserting {len(vectors)} vectors to namespace: {NAMESPACE}")
        response = index.upsert(vectors=vectors, namespace=NAMESPACE)
        print(f"Upsert response: {response}")

        stats = index.describe_index_stats()
        print(f"Index stats after ingestion: {stats}")
    except Exception as e:
        print(f"Error ingesting data: {e}")

if __name__ == "__main__":
    print("Entering main block...")
    file_path = "C:/Users/neilg/vectorscan/fault_data.csv.csv"
    ingest_data(file_path)
    print("Script completed")