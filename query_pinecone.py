import os
from dotenv import load_dotenv
from safe_ai_query import query_fault_description_safe

# This file is now just a clean, simple helper.
# It contains NO Flask-related code (no routes, no app imports).

# Load environment variables
load_dotenv()

def query_fault_description(fault_input, ship_filter):
    """
    This function now has only one job: to call the main AI logic.
    """
    print(f"DEBUG: Calling safe_ai_query with fault: '{fault_input}' and ship: '{ship_filter}'")
    
    # Pass the query along to the script that handles Pinecone and OpenAI
    result = query_fault_description_safe(fault_input, ship_filter=ship_filter)
    
    return result
```

#### **Step 3: Deploy This Final Fix**

1.  **Commit and push** your `fix/startup-crash` branch.
    ```bash
    git add app.py query_pinecone.py
    git commit -m "refactor: Consolidate Flask routes to fix startup crash"
    git push origin fix/startup-crash
    
