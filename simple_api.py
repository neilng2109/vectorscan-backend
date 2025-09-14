from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Simple CORS configuration
CORS(app, origins=["*"], supports_credentials=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "API is working!"})

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simple authentication
    if username == 'admin' and password == 'admin123':
        return jsonify({
            "success": True,
            "token": "simple-jwt-token-12345",
            "message": "Login successful"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401

@app.route('/query', methods=['POST', 'OPTIONS'])
def query():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    fault_input = data.get('fault_input', '')
    
    # Simple mock response
    response = {
        "diagnosis": f"**Diagnosis:** {fault_input} detected.\n**Cause:** System analysis indicates potential equipment malfunction.\n**Resolution:** Inspect and service the affected component."
    }
    
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
