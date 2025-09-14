#!/usr/bin/env python3
"""
Test script to simulate the exact API request flow
"""
import sys
import os
sys.path.append('.')

# Simulate the exact same environment as working_api.py
from safe_ai_query import query_fault_description_safe

print("=== TESTING API FLOW ===")
print("Simulating frontend request: 'pump vibration' for ship 'Iona'")
print()

# This is exactly what working_api.py calls
result = query_fault_description_safe('pump vibration', 'Iona')

print("=== RESULT ===")
print(result)
print()

# Check if it's a mock response
if "Mock response" in result:
    print("❌ ISSUE: Still getting mock response")
    print("The API keys are not being detected properly in the request flow")
elif "AI-powered response" in result:
    print("✅ SUCCESS: AI-powered response working")
else:
    print("❓ UNKNOWN: Response type unclear")
