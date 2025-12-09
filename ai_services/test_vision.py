import requests
import os
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("SERVICE_API_KEY", "sih-2024-secure-key-xyz")

headers = {
    "X-API-Key": API_KEY
}

def create_dummy_image():
    # Create a simple red image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_vision():
    print("\nTesting /quality-check-image...")
    
    image_data = create_dummy_image()
    
    files = {
        'image': ('test.jpg', image_data, 'image/jpeg')
    }
    data = {
        'milletType': 'Bajra'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/quality-check-image", 
            headers=headers, 
            files=files, 
            data=data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_vision()
