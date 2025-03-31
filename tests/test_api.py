import requests
import os
import zipfile
import pandas as pd
import json
from io import BytesIO

def test_api_endpoint(base_url):
    print("🧪 Starting API Tests...\n")
    
    # Test 1: Health Check
    print("Test 1: Health Check")
    try:
        response = requests.get(base_url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")

    # [... rest of the test code remains the same ...]

if __name__ == "__main__":
    # Update the port to match the new port in app.py
    API_URL = "http://127.0.0.1:8000/"
    test_api_endpoint(API_URL)
