import os
import google.generativeai as genai
import json
from typing import List, Dict, Any
from models import MatchProfile
import requests
import random

# --- Configuration & Key Rotation ---
GEMINI_API_KEYS = os.getenv("GEMINI_API_KEYS", "").split(",")
# Clean and filter empty keys
GEMINI_API_KEYS = [k.strip() for k in GEMINI_API_KEYS if k.strip()]

# Fallback to single key if list is empty (though .env should have them)
if not GEMINI_API_KEYS:
    single_key = os.getenv("GEMINI_API_KEY")
    if single_key:
        GEMINI_API_KEYS = [single_key]

# Global index for round-robin rotation
CURRENT_KEY_INDEX = 0

def get_next_key() -> str:
    """Returns the next API key in rotation."""
    global CURRENT_KEY_INDEX
    if not GEMINI_API_KEYS:
        return ""
    key = GEMINI_API_KEYS[CURRENT_KEY_INDEX]
    CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(GEMINI_API_KEYS)
    return key

# Model Name
MODEL_NAME = 'gemini-2.5-flash-lite-preview-09-2025'

def get_gemini_model(api_key: str):
    """Configures and returns a model instance with a specific key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)

GOVT_KEYWORDS = [
    "shree anna", "millet mission", "official scheme", "government benefits", 
    "msp", "pmmsy", "subsidy", "policy", "yojana"
]

# --- Services ---

async def generate_chat_response(query: str, context: str = "") -> Dict[str, Any]:
    # 0. Handle Greeting specifically
    if "namaste" in query.lower() or "hello" in query.lower() or "hi" in query.lower().split():
            return {
            "answer": "Namaste! I am your Millet Assistant. Ask me anything.",
            "sources": []
        }

    # 1. Intent Detection
    SEARCH_KEYWORDS = [
        "shree anna", "millet mission", "official scheme", "government benefits", 
        "msp", "pmmsy", "subsidy", "policy", "yojana",
        "price", "rate", "market", "today", "latest", "news", "current"
    ]
    needs_web_search = any(keyword in query.lower() for keyword in SEARCH_KEYWORDS)

    # RETRY LOOP
    max_retries = len(GEMINI_API_KEYS) + 1
    last_error = None
    
    for attempt in range(max_retries):
        api_key = get_next_key()
        if not api_key:
            return {"answer": "No API keys configured.", "sources": []}

        try:
            if needs_web_search:
                # Web Search Mode logic
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
                
                prompt = f"""
                You are an AI assistant for Indian farmers.
                User Query: {query}
                
                Task:
                1. Search official government websites or news sources for this query.
                2. Extract verified, up-to-date information.
                3. Answer in simple, farmer-friendly English.
                4. List the sources used.
                
                Return a JSON object with:
                - answer: The explanation.
                - sources: List of URLs or source names.
                """
                
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "tools": [{"google_search": {}}]
                }
                
                response = requests.post(url, json=payload)
                
                if response.status_code == 429: # Rate limit
                    print(f"Rate limit hit for key ...{api_key[-4:]}, retrying...")
                    continue
                if response.status_code != 200:
                    last_error = f"API Error: {response.text}"
                    continue # Try next key for other errors too, just in case

                data = response.json()
                # Parse logic
                try:
                    candidate = data.get("candidates", [])[0]
                    text_part = candidate.get("content", {}).get("parts", [])[0].get("text", "")
                    grounding_metadata = candidate.get("groundingMetadata", {})
                    chunks = grounding_metadata.get("groundingChunks", [])
                    sources = [chunk.get("web", {}).get("uri") for chunk in chunks if "web" in chunk]
                    
                    clean_text = text_part.replace("```json", "").replace("```", "").strip()
                    try:
                        result = json.loads(clean_text)
                    except:
                        result = {"answer": clean_text, "sources": sources}
                    
                    if not result.get("sources") and sources:
                        result["sources"] = sources
                    return result
                except Exception as parse_err:
                     # If parsing fails but we got a 200 OK, we probably shouldn't retry with another key, 
                     # but returning the Parse Error is better.
                     return {"answer": "Could not parse response", "sources": []}

            else:
                # Fast Path (SDK)
                model = get_gemini_model(api_key)
                prompt_text = f"""
                You are a helpful Millet Assistant. Answer the following question quickly and concisely.
                Context: {context}
                User: {query}
                Assistant:
                """
                response = model.generate_content(prompt_text)
                return {
                    "answer": response.text,
                    "sources": []
                }
                
        except Exception as e:
            last_error = str(e)
            print(f"Error with key ...{api_key[-4:]}: {e}. Retrying...")
            continue

    return {
        "answer": f"Error generating response after retries: {last_error}",
        "sources": []
    }

async def translate_text(text: str, target_lang: str) -> str:
    max_retries = len(GEMINI_API_KEYS)
    for _ in range(max_retries):
        api_key = get_next_key()
        try:
            model = get_gemini_model(api_key)
            prompt = f"Translate the following text to {target_lang}. Return ONLY the translated text, no explanations.\n\nText: {text}"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            continue
    return "Error translating text (Rate Limit)"

async def get_market_price(millet_type: str, quality_grade: str, location: str) -> Dict:
    max_retries = len(GEMINI_API_KEYS)
    
    for _ in range(max_retries):
        api_key = get_next_key()
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
            prompt = f"""
            Act as an agricultural market expert in India.
            Task:
            1. Search for the CURRENT (last 7 days) market price (mandi price) of {millet_type} in {location} or nearby markets in India.
            2. Establish a realistic Base Price per Quintal (100kg).
            
            Then apply these rules for the Recommended Price:
            - If Quality A (Premium): Price = Base Price + 10%
            - If Quality B (Standard): Price = Base Price
            - If Quality C (Fair): Price = Base Price - 10%
            
            Current Quality: {quality_grade}
            
            Return a JSON object with:
            - market_price (numeric, base price per Quintal)
            - recommended_price (numeric, calculated price per Quintal)
            - currency (string, e.g., "INR")
            - reasoning (string, brief explanation with source if possible, e.g. "Based on average mandi prices in Rajasthan...")
            
            Return ONLY JSON.
            """
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "tools": [{"google_search": {}}]
            }
            
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                continue
                
            data = response.json()
            try:
                candidate = data.get("candidates", [])[0]
                text_part = candidate.get("content", {}).get("parts", [])[0].get("text", "")
                clean_text = text_part.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_text)
            except:
                # If JSON fails, try next key? No, model logic fail, not key fail.
                # But let's return error here.
                return {"market_price": 0, "recommended_price": 0, "currency": "INR", "reasoning": "Parse Error"}
        except Exception:
            continue

    return {"market_price": 0, "recommended_price": 0, "currency": "INR", "reasoning": "Failed to fetch price (All keys exhausted)"}

async def analyze_quality(millet_type: str, description: str, impurities: str) -> Dict:
    max_retries = len(GEMINI_API_KEYS)
    for _ in range(max_retries):
        api_key = get_next_key()
        try:
            model = get_gemini_model(api_key)
            prompt = f"""
            Analyze the quality of this millet sample based on the description.
            Millet Type: {millet_type}
            Description: {description}
            Impurities: {impurities}
            Return a JSON object with: qualityGrade, moistureEstimate, cleanliness, adulterationRisk, recommendation.
            Return ONLY JSON.
            """
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception:
            continue
            
    return {"qualityGrade": "Unknown", "recommendation": "Error: Service Unavailable"}


async def analyze_quality_image(millet_type: str, image_bytes: bytes) -> Dict:
    from PIL import Image
    import io
    
    max_retries = len(GEMINI_API_KEYS)
    for _ in range(max_retries):
        api_key = get_next_key()
        try:
            image = Image.open(io.BytesIO(image_bytes))
            model = get_gemini_model(api_key)
            
            prompt = f"""
            Analyze the quality of this {millet_type} sample based on the image.
            Return a JSON object with:
            - qualityGrade (A, B, or C)
            - moistureEstimate (e.g., "10-12%")
            - cleanliness (High/Medium/Low)
            - adulterationRisk (Low/Medium/High)
            - observedIssues (List of specific visual defects)
            - recommendation (Specific advice)
            Return ONLY JSON.
            """
            
            response = model.generate_content([prompt, image])
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            print(f"Image analysis error with key: {e}")
            continue

    return {
        "qualityGrade": "Unknown",
        "observedIssues": ["Error processing image"],
        "recommendation": "Service Unavailable"
    }

async def match_users(user_type: str, millet_type: str, quantity: float, location: str) -> List[MatchProfile]:
    candidates = MOCK_BUYERS if user_type == "farmer" else MOCK_FARMERS
    candidates_json = json.dumps([c.__dict__ for c in candidates])
    
    max_retries = len(GEMINI_API_KEYS)
    for _ in range(max_retries):
        api_key = get_next_key()
        try:
            model = get_gemini_model(api_key)
            prompt = f"""
            Act as a B2B agricultural matching engine.
            My Profile: {user_type}, {millet_type}, {quantity} kg, {location}
            Potential Matches: {candidates_json}
            Task: Score matches (0-100) based on type, location, quantity. Return ONLY candidates with score > 50 in JSON array.
            """
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            matches_data = json.loads(text)
            matches = []
            for m in matches_data:
                matches.append(MatchProfile(
                    id=m.get("id"), name=m.get("name"), type=m.get("type"),
                    millet_type=m.get("millet_type"), quantity=m.get("quantity"),
                    location=m.get("location")
                ))
            return matches
        except Exception:
            continue
            
    # Fallback
    return [c for c in candidates if millet_type.lower() in c.millet_type.lower()]

async def get_market_trends(millet_type: str) -> List[Dict[str, Any]]:
    max_retries = len(GEMINI_API_KEYS)
    for _ in range(max_retries):
        api_key = get_next_key()
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
            prompt = f"Search daily wholesale market prices of {millet_type} in major Indian mandis for last 15-30 days. Return JSON array with date, price_per_quintal, market_name."
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "tools": [{"google_search": {}}]
            }
            
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                continue
            
            data = response.json()
            candidate = data.get("candidates", [])[0]
            text_part = candidate.get("content", {}).get("parts", [])[0].get("text", "")
            clean_text = text_part.replace("```json", "").replace("```", "").strip()
            start = clean_text.find("[")
            end = clean_text.rfind("]") + 1
            if start != -1 and end != -1:
                clean_text = clean_text[start:end]
            return json.loads(clean_text)
        except Exception:
            continue
            
    return []

# Mocks
MOCK_FARMERS = [
    MatchProfile(id="f1", name="Ramesh Kumar", type="farmer", millet_type="Pearl Millet", quantity=100, location="Rajasthan"),
    MatchProfile(id="f2", name="Suresh Singh", type="farmer", millet_type="Sorghum", quantity=500, location="Maharashtra"),
    MatchProfile(id="f3", name="Anita Devi", type="farmer", millet_type="Finger Millet", quantity=200, location="Karnataka"),
    MatchProfile(id="f4", name="Rajesh Gupta", type="farmer", millet_type="Foxtail Millet", quantity=150, location="Andhra Pradesh"),
    MatchProfile(id="f5", name="Vikram Singh", type="farmer", millet_type="Pearl Millet", quantity=300, location="Gujarat"),
]
MOCK_BUYERS = [
    MatchProfile(id="b1", name="Millet Foods Ltd", type="buyer", millet_type="Pearl Millet", quantity=1000, location="Delhi"),
    MatchProfile(id="b2", name="Healthy Grains", type="buyer", millet_type="Finger Millet", quantity=150, location="Bangalore"),
]
