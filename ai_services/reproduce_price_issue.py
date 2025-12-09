import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERVICE_API_KEY", "sih-2024-secure-key-xyz")
URL = "http://127.0.0.1:8000/price-gemini"

payload = {
    "millet_type": "Foxtail Millet",
    "quality_grade": "A",
    "location": "Jaipur"
}

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print(f"--- Testing Price Prediction ---")
print(f"URL: {URL}")
print(f"Payload: {payload}")

try:
    response = requests.post(URL, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    try:
        print("Response JSON:")
        print(response.json())
    except:
        print("Response Text:")
        print(response.text)
except Exception as e:
    print(f"Request Failed: {e}")
