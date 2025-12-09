from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()
# Force reload trigger

from models import (
    ChatRequest, ChatResponse,
    TranslateRequest, TranslateResponse,
    PriceRequest, PriceResponse,
    MatchRequest, MatchResponse,
    QualityCheckRequest, QualityCheckResponse,
    MarketTrendRequest, MarketTrendResponse
)

import services

app = FastAPI(
    title="Millet Marketplace AI Services",
    description="Microservices for Chatbot, Translation, Price Prediction, Matching, and Quality Check",
    version="1.0.0"
)

# CORS Configuration
# Allow requests from the frontend domain
origins = [
    "http://localhost:3000",
    "https://shree-anna-connect-644bd4aa.base44.app", # Frontend URL
    "*" # For testing, restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security: API Key Validation
API_KEY_NAME = "X-API-Key"
EXPECTED_API_KEY = os.getenv("SERVICE_API_KEY", "default-insecure-key")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "Millet AI Services are running. Use /docs for API documentation."}

@app.post("/chatbot", response_model=ChatResponse)
async def chatbot(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """
    General conversational assistant for farmers.
    Supports government scheme queries with web search.
    """
    result = await services.generate_chat_response(request.query, request.context)
    return ChatResponse(**result)

@app.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest, api_key: str = Depends(verify_api_key)):
    """
    Translates text between English, Hindi, and Bengali.
    """
    translated = await services.translate_text(request.text, request.target_language)
    return TranslateResponse(
        translated_text=translated,
        original_text=request.text,
        language=request.target_language
    )

@app.post("/price-gemini", response_model=PriceResponse)
async def price_check(request: PriceRequest, api_key: str = Depends(verify_api_key)):
    """
    Predicts market price and recommends selling price based on quality.
    """
    result = await services.get_market_price(request.millet_type, request.quality_grade, request.location)
    return PriceResponse(**result)

@app.post("/match", response_model=MatchResponse)
async def match_users(request: MatchRequest, api_key: str = Depends(verify_api_key)):
    """
    Matches farmers and buyers based on millet type and location.
    """
    matches = await services.match_users(request.user_type, request.millet_type, request.quantity, request.location)
    return MatchResponse(matches=matches)

@app.post("/quality-check", response_model=QualityCheckResponse)
async def quality_check(request: QualityCheckRequest, api_key: str = Depends(verify_api_key)):
    """
    Analyzes millet quality based on description and impurities.
    """
    result = await services.analyze_quality(request.millet_type, request.description, request.impurities)
    # Ensure observedIssues is present for compatibility
    if "observedIssues" not in result:
        result["observedIssues"] = []
    return QualityCheckResponse(**result)

from fastapi import File, UploadFile, Form

@app.post("/quality-check-image", response_model=QualityCheckResponse)
async def quality_check_image(
    milletType: str = Form(...),
    image: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    """
    Analyzes millet quality based on an uploaded image using Gemini Vision.
    """
    image_bytes = await image.read()
    result = await services.analyze_quality_image(milletType, image_bytes)

    return QualityCheckResponse(**result)

@app.post("/market-trends", response_model=MarketTrendResponse)
async def market_trends(request: MarketTrendRequest, api_key: str = Depends(verify_api_key)):
    """
    Fetches real market trends using Gemini Search.
    """
    trends = await services.get_market_trends(request.millet_type)
    return MarketTrendResponse(trends=trends)

# --- Product Endpoints (SQLite) ---
from models import ProductCreate, ProductUpdate
import database

@app.get("/products")
async def get_products(seller_id: Optional[str] = None):
    """
    Get all products or filter by seller_id.
    """
    return database.get_products(seller_id)

@app.post("/products")
async def create_product(product: ProductCreate, api_key: str = Depends(verify_api_key)):
    """
    Create a new product.
    """
    return database.create_product(product.dict())

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdate, api_key: str = Depends(verify_api_key)):
    """
    Update an existing product.
    """
    updated_product = database.update_product(product_id, product.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, api_key: str = Depends(verify_api_key)):
    """
    Delete a product.
    """
    success = database.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
