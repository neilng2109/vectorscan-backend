import os
import json
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
    Performs a RAG query and returns a simple, formatted string for the UI.
    """
    if not PINECONE_API_KEY or not OPENAI_API_KEY:
        return "Error: API keys not configured."

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
        
        context = ""
        if results.matches:
            for match in results.matches:
                metadata = match.metadata
                context += f"Similar fault: {metadata.get('fault', 'N/A')} on {metadata.get('equipment', 'N/A')} - {metadata.get('cause', 'N/A')}. Resolution: {metadata.get('resolution', 'N/A')}\n"
        else:
            context = "No similar faults found."
        
        # --- SIMPLE, STABLE PROMPT ---
        prompt = (
            f"You are a maritime fault diagnosis expert.\n"
            f"Fault: '{fault_input}'\n"
            f"Similar past faults:\n{context}\n\n"
            f"Provide a concise diagnosis with cause and resolution.\n"
            f"Format as: **Diagnosis:** [text]\n"
            f"**Cause:** [text]\n"
            f"**Resolution:** [text]"
        )

        ai_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200 
        )
        
        diagnosis = ai_response.choices[0].message.content.strip()
        
        # Add a simple status footer
        diagnosis += "\n\n**Status:** AI-powered response with Pinecone similarity search"
        
        return diagnosis

    except Exception as e:
        return f"Error during AI query: {str(e)}."

