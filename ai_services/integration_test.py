
import requests
import json
import sys

# LOCALHOST URLs
CHAT_URL = "http://localhost:8000/chatbot"
PRICE_URL = "http://localhost:8000/market-trends"

def test_chat():
    print("1. Testing Local Chatbot Endpoint...")
    try:
        payload = {"query": "What is finger millet?", "context": "User is a farmer."}
        # Provide the SERVICE KEY header if needed, but for now we look at local execution
        headers = {"X-API-Key": "your_secure_internal_key_here"} # Default from .env or code
        
        response = requests.post(CHAT_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Chat Success: {response.json().get('answer')[:50]}...")
            return True
        else:
            print(f"❌ Chat Fail: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat Exception: {e}")
        return False

def test_trends():
    print("\n2. Testing Local Market Trends Endpoint (Real Data Fetch)...")
    try:
        payload = {"millet_type": "Pearl Millet"}
        headers = {"X-API-Key": "your_secure_internal_key_here"}
        
        response = requests.post(PRICE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            trends = data.get("trends", [])
            print(f"✅ Trends Success: Found {len(trends)} records.")
            if trends:
                print(f"   Sample: {trends[0]}")
            return True
        else:
            print(f"❌ Trends Fail: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Trends Exception: {e}")
        return False

if __name__ == "__main__":
    if test_chat() and test_trends():
         print("\n✅✅ PRODUCTION GRADE INTEGRATION TEST PASSED")
    else:
         print("\n❌❌ INTEGRATION TEST FAILED")
