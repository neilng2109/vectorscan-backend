# Import required libraries
from dotenv import load_dotenv
import os
from pinecone import Pinecone
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Access the Pinecone API key from the .env file
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY not found in .env file")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("vectorscan-faults")

# Load the CSV file
try:
    csv_data = pd.read_csv("fault_data.csv")  # Ensure the file is in the same directory or provide the full path
    record_ids = csv_data["Fault Entry ID"].tolist()
    print("CSV file loaded successfully. Found", len(record_ids), "records.")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit(1)

# Fetch vectors with metadata
try:
    fetch_response = index.fetch(ids=record_ids, namespace="")
    print("Fetch response received successfully.")
except Exception as e:
    print(f"Error fetching vectors: {e}")
    exit(1)

# Verify metadata for each record and cross-check with CSV
for record_id in record_ids:
    vector = fetch_response.vectors.get(record_id)
    csv_row = csv_data[csv_data["Fault Entry ID"] == record_id].iloc[0] if not csv_data[csv_data["Fault Entry ID"] == record_id].empty else None
    print(f"\nRecord ID: {record_id}")
    if vector:
        if hasattr(vector, "metadata") and vector.metadata:
            print(f"Pinecone Metadata for {record_id}: {vector.metadata}")
            if "fault" in vector.metadata:
                print(f"fault from Pinecone: {vector.metadata['fault']}")
            else:
                print(f"No 'fault' found in Pinecone metadata for {record_id}")
        else:
            print(f"No metadata found for {record_id}")
        # Cross-check with CSV
        if csv_row is not None:
            print(f"CSV Data for {record_id}: Equipment={csv_row['Equipment Affected']}, Fault={csv_row['Fault Description']}")
            if "fault" in vector.metadata and vector.metadata["fault"] == csv_row["Fault Description"]:
                print("Fault matches between Pinecone and CSV.")
            else:
                print("Fault mismatch between Pinecone and CSV.")
        else:
            print(f"No matching record found in CSV for {record_id}")
    else:
        print(f"Record {record_id} not found in Pinecone fetch response.")