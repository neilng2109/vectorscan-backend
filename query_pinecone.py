from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from safe_ai_query import query_fault_description_safe

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
print("Loaded env - PINECONE_API_KEY:", bool(os.getenv("PINECONE_API_KEY")))

app = Flask(__name__)

# --- START OF FIX ---
# Define the complete list of allowed frontend domains
allowed_origins = [
    "https://vectorscan.io",                 # The naked domain
    "https://www.vectorscan.io",             # The www subdomain
    "https://iridescent-sunburst-b70f4e.netlify.app" # Your Netlify preview URL
]

# Apply the CORS settings with the full list
CORS(app, origins=allowed_origins, supports_credentials=True, methods=["GET", "POST", "OPTIONS"])
# --- END OF FIX ---

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secure-key')
jwt = JWTManager(app)

users = {
    'engineer_iona': {'password': 'pass123', 'role': 'ETO_Iona', 'ship': 'Iona'},
    'engineer_wonder': {'password': 'pass456', 'role': 'ETO_Wonder', 'ship': 'Wonder of the Seas'},
    'engineer_wind': {'password': 'pass789', 'role': 'ETO_WindSurf', 'ship': 'Wind Surf'},
    'admin': {'password': 'admin123', 'role': 'Admin', 'ship': 'All'}
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username]['password'] == password:
        access_token = create_access_token(identity={'username': username, 'role': users[username]['role'], 'ship': users[username]['ship']})
        return jsonify({'token': access_token, 'user': {'username': username, 'role': users[username]['role'], 'ship': users[username]['ship']}}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# 1. The new, importable logic function
# It takes the necessary data as arguments instead of getting them from the web request.
def query_fault_description(fault_input, ship):
    """
    Queries the vector database for a fault description, filtered by ship.
    """
    # This is the function that actually queries Pinecone and OpenAI
    # The name might be slightly different in your code.
    result = query_fault_description_safe(fault_input, ship_filter=ship)

    # ---- ADD THIS PRINT STATEMENT ----
    # See what Pinecone is returning. Is it an empty list?
    print(f"DEBUG: Context from Pinecone for ship '{ship}': {result}")
    
    return result

# 2. The lean and clean Flask route handler
# Its only job is to handle the web request and call the logic function.
@app.route('/query', methods=['POST'])
@jwt_required()
def query_fault():
    # Get user info from the JWT token
    current_user = get_jwt_identity()
    ship = current_user['ship']
    
    # Get the fault description from the incoming JSON
    data = request.json
    if not data or not data.get('fault_description'):
        return jsonify({'error': 'Fault input required'}), 400
    
    fault_input = data.get('fault_description').strip()
    
    # --- Call the logic function ---
    result = query_fault_description(fault_input, ship)
    
    # Send the final response back to the browser
    return jsonify({
        'result': result,
        'fault_description': fault_input,
        'ship': ship,
        'user': current_user['username']
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'VectorScan API'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

