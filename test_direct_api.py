#!/usr/bin/env python3
"""
Test direct API calls to isolate frontend/backend disconnect
"""
import requests
import json

API_BASE = "http://127.0.0.1:5000"

print("=== TESTING DIRECT API CALLS ===")
print()

# Test 1: Health check
print("1. Testing health endpoint...")
try:
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
print()

# Test 2: Debug query (no auth)
print("2. Testing debug-query endpoint (no auth)...")
try:
    payload = {
        "fault_description": "pump vibration",
        "ship_filter": "Iona"
    }
    response = requests.post(
        f"{API_BASE}/debug-query",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Check if AI or mock
    result = response.json().get("result", "")
    if "AI-powered response" in result:
        print("✅ SUCCESS: AI-powered response received!")
    elif "Mock response" in result:
        print("❌ ISSUE: Still getting mock response")
    else:
        print("❓ UNCLEAR: Response type unknown")
        
except Exception as e:
    print(f"Error: {e}")
print()

# Test 3: Login to get JWT token
print("3. Testing login...")
try:
    login_payload = {
        "username": "engineer_iona",
        "password": "pass123"
    }
    response = requests.post(
        f"{API_BASE}/login",
        json=login_payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    login_result = response.json()
    print(f"Login success: {login_result.get('success')}")
    
    if login_result.get("success"):
        token = login_result.get("token")
        print(f"Token received: {token[:50]}...")
        
        # Test 4: Authenticated query
        print()
        print("4. Testing authenticated query endpoint...")
        query_payload = {
            "fault_description": "pump vibration",
            "ship_filter": "Iona"
        }
        response = requests.post(
            f"{API_BASE}/query",
            json=query_payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check if AI or mock
        result = response.json().get("result", "")
        if "AI-powered response" in result:
            print("✅ SUCCESS: AI-powered response received via authenticated endpoint!")
        elif "Mock response" in result:
            print("❌ ISSUE: Still getting mock response via authenticated endpoint")
        else:
            print("❓ UNCLEAR: Response type unknown")
    
except Exception as e:
    print(f"Error: {e}")

print()
print("=== TEST COMPLETE ===")
