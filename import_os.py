import os
import pandas as pd
from pyairtable import Api

# Configuration
API_KEY = "patp4aRP6XDBzg4BN.9de61e670e4536b48fb35d66d685fb16c1f839b9a3c53e9d131bc0750cd5af2b"
BASE_ID = "appou9WDI7YE76kIR"
TABLE_NAME = "Fault History Table"

# Initialize Airtable API
api = Api(API_KEY)
table = api.table(BASE_ID, TABLE_NAME)

def extract_data():
    try:
        # Fetch all records
        records = table.all()
        data = []

        # Extract data fields
        for record in records:
            fields = record["fields"]
            data.append({
                "Fault Entry ID": record["id"],
                "Equipment Affected": fields.get("Equipment Affected", ""),
                "Fault Description": fields.get("Fault Description", ""),
                "Cause (if known)": fields.get("Cause (if known)", ""),
                "Resolution Action": fields.get("Resolution Action", "")
            })

        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(data)
        csv_path = "fault_data.csv"
        df.to_csv(csv_path, index=False)
        print(f"Data successfully extracted to {csv_path}")

    except Exception as e:
        print(f"Error extracting data: {e}")

if __name__ == "__main__":
    extract_data()
