import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("SERVICE_API_KEY", "sih-2024-secure-key-xyz")

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def test_root():
    print("\nTesting Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

def test_chatbot():
    print("\nTesting /chatbot...")
    payload = {
        "message": "How do I grow millet?",
        "context": "I am a farmer in Rajasthan."
    }
    try:
        response = requests.post(f"{BASE_URL}/chatbot", headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

def test_translate():
    print("\nTesting /translate...")
    payload = {
        "text": "Hello, how are you?",
        "target_language": "hi"
    }
    try:
        response = requests.post(f"{BASE_URL}/translate", headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

def test_price():
    print("\nTesting /price-gemini...")
    payload = {
        "millet_type": "Bajra",
        "quality_grade": "A",
        "location": "Jaipur"
    }
    try:
        response = requests.post(f"{BASE_URL}/price-gemini", headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

def test_match():
    print("\nTesting /match...")
    payload = {
        "user_type": "farmer",
        "millet_type": "Bajra",
        "quantity": 100,
        "location": "Delhi"
    }
    try:
        response = requests.post(f"{BASE_URL}/match", headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

def test_quality():
    print("\nTesting /quality-check...")
    payload = {
        "millet_type": "Ragi",
        "description": "Reddish brown, small grains",
        "impurities": "None"
    }
    try:
        response = requests.post(f"{BASE_URL}/quality-check", headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_root()
    test_match() # This one doesn't need Gemini
    test_chatbot()
    test_translate()
    test_price()
    test_quality()
