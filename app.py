from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from query_pinecone import query_fault_description

app = Flask(__name__)

# Enable CORS for all routes - simplified configuration to fix login issue
CORS(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secure-key')
jwt = JWTManager(app)

# Mock user database
users = {
    'engineer_iona': {'password': 'pass123', 'role': 'ETO_Iona', 'ship': 'Iona'},
    'engineer_wonder': {'password': 'pass456', 'role': 'ETO_Wonder', 'ship': 'Wonder of the Seas'},
    'engineer_wind': {'password': 'pass789', 'role': 'ETO_WindSurf', 'ship': 'Wind Surf'},
    'admin': {'password': 'admin123', 'role': 'Admin', 'ship': 'All'}
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'VectorScan API'}), 200

@app.route('/login', methods=['POST'])
def login():
    """Authentication endpoint"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if username in users and users[username]['password'] == password:
            access_token = create_access_token(
                identity={
                    'username': username, 
                    'role': users[username]['role'], 
                    'ship': users[username]['ship']
                }
            )
            return jsonify({
                'token': access_token,
                'user': {
                    'username': username,
                    'role': users[username]['role'],
                    'ship': users[username]['ship']
                }
            }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")  # For debugging
        return jsonify({'error': f'Login error: {str(e)}'}), 500

@app.route('/query', methods=['POST'])
@jwt_required()
def query_fault():
    """Fault diagnosis query endpoint"""
    try:
        current_user = get_jwt_identity()
        ship = current_user['ship']
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        fault_input = data.get('fault_description', '').strip()  # Changed to match frontend parameter
        if not fault_input:
            return jsonify({'error': 'Fault description required'}), 400
        
        # Use AI-powered Pinecone query for real maritime fault diagnosis
        result = query_fault_description(fault_input, ship_filter=ship)
        
        return jsonify({
            'result': result,
            'fault_input': fault_input,
            'ship': ship,
            'user': current_user['username']
        }), 200
        
    except Exception as e:
        print(f"Query error: {str(e)}")  # For debugging
        # Fallback response if AI service is unavailable
        current_user = get_jwt_identity()
        ship = current_user.get('ship', 'Unknown')
        fault_input = request.json.get('fault_input', 'Unknown fault') if request.json else 'Unknown fault'
        
        fallback_result = f"AI service temporarily unavailable. Fault logged: {fault_input} on {ship}. Please contact technical support."
        return jsonify({
            'result': fallback_result, 
            'error': str(e),
            'fallback': True
        }), 200

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """Get current user information"""
    current_user = get_jwt_identity()
    return jsonify({'user': current_user}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"Server error: {str(error)}")  # For debugging
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)