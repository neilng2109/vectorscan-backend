import os
import pandas as pd
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone and OpenAI
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the index name
index_name = "vectorscan-faults"

# Create the index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index(index_name)

# Load the fault database
fault_data = pd.read_csv("fault_data.csv")

# Debug: Print the column names
print("Columns in fault_data.csv:", fault_data.columns.tolist())

# Handle NaN values by filling with defaults
fault_data['Equipment Affected'] = fault_data['Equipment Affected'].fillna('Unknown Equipment')
fault_data['Fault Description'] = fault_data['Fault Description'].fillna('Unknown Fault')

# Combine fields for embedding, with fallback for missing columns
fault_data['embedding_text'] = fault_data.apply(
    lambda row: f"{row['Equipment Affected']} {row['Fault Description']}: No symptoms recorded",
    axis=1
)

# Generate embeddings using the new OpenAI API
embeddings = []
for text in fault_data['embedding_text']:
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    embeddings.append(response.data[0].embedding)
fault_data['embedding'] = embeddings

# Prepare vectors for upsert with corrected metadata keys
vectors = []
for i, row in fault_data.iterrows():
    # Derive a diagnosis
    diagnosis = f"{row['Equipment Affected']} experienced {row['Fault Description'].lower()}"
    vectors.append({
        "id": str(row.get('Fault Entry ID', i)),  # Fallback to row index if ID is missing
        "values": row['embedding'],
        "metadata": {
            "equipment_affected": row['Equipment Affected'],
            "fault_description": row['Fault Description'],
            "symptoms_observed": "No symptoms recorded",  # Column missing
            "cause": row.get('Cause (if known)', 'Unknown') if pd.notna(row.get('Cause (if known)', 'Unknown')) else "Unknown",
            "resolution_action": row.get('Resolution Action', 'Not resolved') if pd.notna(row.get('Resolution Action', 'Not resolved')) else "Not resolved",
            "date_of_fault": "Unknown",  # Column missing
            "equipment_id": "Unknown",  # Column missing
            "system_type": "Unknown",  # Column missing
            "fault_code": "Unknown",  # Column missing
            "diagnosis": diagnosis
        }
    })

# Upsert vectors in batches
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    index.upsert(vectors=batch)

print(f"Successfully ingested {len(vectors)} faults into Pinecone index '{index_name}'.")