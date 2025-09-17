import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize clients
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("vectorscan-faults")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def query_fault_description_safe(fault_input, ship_filter=None):
    """
    Performs a RAG query and returns a structured JSON for the UI.
    """
    if not PINECONE_API_KEY or not OPENAI_API_KEY:
        return {"error": "API keys not configured."}

    try:
        # Step 1: Create embedding for the user's input
        response = openai_client.embeddings.create(input=fault_input, model="text-embedding-ada-002")
        fault_embedding = response.data[0].embedding

        # Step 2: Query Pinecone for similar historical faults
        query_filter = {"ship": {"$eq": ship_filter}} if ship_filter and ship_filter != 'all' else None
        results = index.query(
            vector=fault_embedding,
            top_k=3,
            include_metadata=True,
            filter=query_filter
        )
        
        # Parse similar faults into structured list
        similar_faults = []
        if results.matches:
            for match in results.matches:
                metadata = match.metadata
                similar_faults.append({
                    "equipment": metadata.get('equipment', 'N/A'),
                    "fault": metadata.get('fault', 'N/A'),
                    "resolution": metadata.get('resolution', 'N/A'),
                    "date": metadata.get('date', 'N/A'),
                    "id": metadata.get('id', None),
                    "cause": metadata.get('cause', 'N/A')
                })
            context_for_prompt = "\n".join([
                f"Equipment: {fault['equipment']} | Fault: {fault['fault']} | Cause: {fault['cause']} | Resolution: {fault['resolution']}" 
                for fault in similar_faults
            ])
        else:
            context_for_prompt = "No similar faults found."

        # --- RICH PROMPT ---
        prompt = (
            f"You are a maritime fault diagnosis expert.\n"
            f"Fault description: '{fault_input}'\n"
            f"Similar past faults:\n{context_for_prompt}\n\n"
            f"Reply with:\n"
            f"Title: [short fault diagnosis title]\n"
            f"Diagnosis: [single sentence]\n"
            f"Recommended Actions:\n- [action 1]\n- [action 2]\n- [action 3]\n"
        )

        ai_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        ai_text = ai_response.choices[0].message.content.strip()

        # Parse AI response into fields
        title_match = re.search(r"Title:\s*(.*)", ai_text)
        diagnosis_match = re.search(r"Diagnosis:\s*(.*)", ai_text)
        actions_match = re.search(r"Recommended Actions:\s*((?:- .*\n?)+)", ai_text)

        fault_title = title_match.group(1).strip() if title_match else fault_input + " Diagnosis"
        diagnosis = diagnosis_match.group(1).strip() if diagnosis_match else ""
        actions = []
        if actions_match:
            actions = [line[2:].strip() for line in actions_match.group(1).strip().splitlines() if line.startswith('- ')]
        status = "AI-powered response with Pinecone similarity search"

        return {
            "fault_title": fault_title,
            "diagnosis": diagnosis,
            "recommended_actions": actions,
            "similar_faults": similar_faults,
            "status": status
        }

    except Exception as e:
        return {"error": f"Error during AI query: {str(e)}."}