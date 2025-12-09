
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Read models from file or fetch fresh
try:
    models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            models.append(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
    models = ["models/gemini-2.5-flash", "models/gemini-2.0-flash-exp", "models/gemini-flash-latest"]

print(f"Testing {len(models)} models...")
print("-" * 50)

working_models = []

for model_name in models:
    print(f"Testing {model_name}...", end=" ", flush=True)
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi", request_options={"timeout": 10})
        print(f"✅ SUCCESS")
        working_models.append(model_name)
    except Exception as e:
        error_str = str(e)
        if "429" in error_str:
            print("❌ 429 (Quota/Rate Limit)")
        elif "404" in error_str:
            print("❌ 404 (Not Found)")
        else:
            print(f"❌ Error: {error_str[:50]}...")
    
    # Small delay to avoid hitting rate limits just by testing
    time.sleep(1)

print("-" * 50)
print("WORKING MODELS:")
for m in working_models:
    print(f"- {m}")
