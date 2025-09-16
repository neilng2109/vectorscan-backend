import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
# We now import the logic function directly
from query_pinecone import query_fault_description

load_dotenv()
app = Flask(__name__)

# --- DYNAMIC CORS CONFIGURATION ---
allowed_origins_str = os.environ.get('CORS_ORIGINS')
if not allowed_origins_str:
    allowed_origins = ["http://localhost:5173"] 
else:
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',')]
print(f"CORS is configured for the following origins: {allowed_origins}")
CORS(app, origins=allowed_origins, supports_credentials=True)

# --- JWT AND USER CONFIG ---
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-super-secret-key-for-dev')
jwt = JWTManager(app)

users = {
    'engineer_iona': {'password': 'pass123', 'role': 'ETO_Iona', 'ship': 'Iona'},
    'admin': {'password': 'admin123', 'role': 'Admin', 'ship': 'All'}
}

# --- API ROUTES ---

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if user and user['password'] == password:
        identity_data = { "username": username, "role": user['role'], "ship": user['ship'] }
        access_token = create_access_token(identity=identity_data)
        return jsonify(token=access_token)
    
    return jsonify({"error": "Invalid credentials"}), 401

# --- THE /query ROUTE IS NOW MOVED HERE ---
@app.route('/query', methods=['POST'])
@jwt_required()
def query_endpoint():
    current_user = get_jwt_identity()
    ship = current_user.get('ship')
    
    data = request.json
    if not data or not data.get('fault_description'):
        return jsonify({'error': 'Fault description is required'}), 400
        
    fault_input = data.get('fault_description').strip()
    # We call the clean logic function from our other file
    result_text = query_fault_description(fault_input, ship)
    
    return jsonify({
        'result': result_text,
        'fault_description': fault_input,
        'ship': ship,
        'user': current_user.get('username')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

