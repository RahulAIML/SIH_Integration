
import asyncio
import os
import requests
import json
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEYS = os.getenv("GEMINI_API_KEYS", "").split(",")
if not GEMINI_API_KEYS:
    GEMINI_API_KEYS = [os.getenv("GEMINI_API_KEY")]
    
import random
MODEL_NAME = 'gemini-2.5-flash-preview-09-2025'
# Pick a random key to start
api_key = random.choice(GEMINI_API_KEYS)

async def test_trends_real():
    print(f"Testing real trends with Key: ...{api_key[-4:]}")
    print(f"Model: {MODEL_NAME}")
    
    millet_type = "Pearl Millet (Bajra)"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
            
    # VERY STRICT PROMPT for Real Data
    prompt = f"""
    Context: You are a data extraction bot for Indian Agricultural Markets (Mandis).
    Task: Search specifically for "Agmarknet daily mandi rates {millet_type}" for the last 15 days.
    
    Examine the search results for:
    - Date (YYYY-MM-DD)
    - Market Name (e.g. Jaipur, Alwar, Nizamabad)
    - Price (in INR per Quintal)

    Extract at least 5-10 REAL data points found in the search snippets. 
    DO NOT GENERATE DUMMY DATA. If you find no specific data, return an empty array.
    
    Return ONLY valid JSON Array:
    [
        {{"date": "2024-10-25", "market_name": "Alwar", "price_per_quintal": 2150}},
        ...
    ]
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}]
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return

        data = response.json()
        
        # Check grounding (did it search?)
        candidate = data.get("candidates", [])[0]
        grounding = candidate.get("groundingMetadata", {})
        print(f"\nGrounding (Search Performed?): {grounding.get('searchEntryPoint', 'No Search Data')}")
        
        text_part = candidate.get("content", {}).get("parts", [])[0].get("text", "")
        print("\n--- Raw Response ---")
        print(text_part)
        print("--------------------\n")
        
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_trends_real())
