import requests
import json
import os

API_URL = "http://127.0.0.1:8000/chatbot"
API_KEY = "sih-2024-secure-key-xyz"  # Matching the .env value

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def test_query(query_text):
    print(f"\n--- Testing Query: '{query_text}' ---")
    payload = {
        "query": query_text,
        "context": "Test context"
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Error Response:")
            print(response.text)
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    # 1. Test Normal Query
    test_query("Hello, how are you?")
    
    # 2. Test Govt Scheme Query (Triggers Search)
    test_query("What are the benefits of Shree Anna Abhiyan?")
