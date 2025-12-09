
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

candidate = "gemini-2.5-flash-lite-preview-09-2025"
print(f"Testing candidate: {candidate}")

try:
    model = genai.GenerativeModel(candidate)
    response = model.generate_content("Hello")
    print("Response received:")
    print(response.text)
    print("✅ VERIFIED WORKING")
except Exception as e:
    print(f"❌ FAILED: {e}")
