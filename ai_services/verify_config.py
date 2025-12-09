
from services import MODEL_NAME
import os

print(f"Current Configured Model: {MODEL_NAME}")
if MODEL_NAME == 'gemini-2.5-flash-lite-preview-09-2025':
    print("✅ Verified: Using Gemini 2.5 Flash Lite Preview everywhere.")
else:
    print(f"❌ Mismatch! Found {MODEL_NAME}")
