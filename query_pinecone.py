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

### Your Next Steps

1.  **Replace the Content of `app.py`:** Go to your `app.py` file, delete everything inside it (including all the conflict markers), and paste the code from the **"Updated app.py (Resolved Conflicts)"** file above.
2.  **Replace the Content of `query_pinecone.py`:** Go to your `query_pinecone.py` file, delete everything inside it, and paste the code from the **"Simplified query_pinecone.py (Logic Only)"** file above.
3.  **Save both files.**
4.  **Finalize the Merge:** Now that the files are fixed, run these final commands in your terminal to complete the process.

    ```bash
    # 1. Stage the files you just fixed. This tells Git the conflict is resolved.
    git add app.py query_pinecone.py

    # 2. Commit your changes. Git will know you're finishing the merge.
    git commit -m "refactor: Consolidate Flask routes and resolve merge conflict"

    # 3. Push the final, correct version to GitHub.
    git push origin fix/startup-crash
    

