
import google.generativeai as genai
import os
import requests
import sys

# EXPLICIT KEY FROM USER
API_KEY = "AIzaSyDEyP_8ojLvAmruR-6CsMf_Kh0dyfosbpc"
MODEL_NAME = "gemini-2.5-flash-lite-preview-09-2025"

print(f"--- DIAGNOSTIC START ---")
print(f"Key: ...{API_KEY[-8:]}")
print(f"Model: {MODEL_NAME}")

def test_genai_sdk():
    print("\n1. Testing Google GenerativeAI SDK...")
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content("Explain 'Millet' in 5 words.")
        print(f"✅ SDK Success: {response.text}")
        return True
    except Exception as e:
        print(f"❌ SDK FAIL: {e}")
        return False

def test_rest_api():
    print("\n2. Testing REST API (HTTP POST)...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": "Explain 'Millet' in 5 words."}]}]}
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
             print(f"✅ REST Success: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
             return True
        else:
             print(f"❌ REST FAIL: {response.text}")
             return False
    except Exception as e:
        print(f"❌ REST Exception: {e}")
        return False

if __name__ == "__main__":
    sdk_ok = test_genai_sdk()
    rest_ok = test_rest_api()
    
    if sdk_ok and rest_ok:
        print("\n✅✅ CRITICAL SYSTEM CHECK PASSED: API Key and Model are working.")
        sys.exit(0)
    else:
        print("\n❌❌ SYSTEM CHECK FAILED: Verification Required.")
        sys.exit(1)
