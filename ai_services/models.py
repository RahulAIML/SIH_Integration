from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Chatbot
# Chatbot
class ChatRequest(BaseModel):
    query: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []

# Translate
class TranslateRequest(BaseModel):
    text: str
    target_language: str # 'hi', 'bn', 'en'
    source_language: Optional[str] = 'auto'

class TranslateResponse(BaseModel):
    translated_text: str
    original_text: str
    language: str

# Price Check
class PriceRequest(BaseModel):
    millet_type: str
    quality_grade: str # A, B, C
    location: Optional[str] = "India"

class PriceResponse(BaseModel):
    market_price: float
    recommended_price: float
    currency: str
    reasoning: str

# Match
class MatchRequest(BaseModel):
    user_type: str # 'farmer' or 'buyer'
    millet_type: str
    quantity: float
    location: str

class MatchProfile(BaseModel):
    id: str
    name: str
    type: str
    millet_type: str
    quantity: float
    location: str
    distance_km: Optional[float] = None

class MatchResponse(BaseModel):
    matches: List[MatchProfile]

# Quality Check
class QualityCheckRequest(BaseModel):
    millet_type: str
    description: str
    impurities: Optional[str] = None

class QualityCheckResponse(BaseModel):
    qualityGrade: str # A, B, C
    moistureEstimate: str
    cleanliness: str
    adulterationRisk: str
    observedIssues: List[str]
    recommendation: str

# Market Trends
class MarketTrendRequest(BaseModel):
    millet_type: str

class MarketTrendDataPoint(BaseModel):
    date: str
    price_per_quintal: float
    market_name: str

class MarketTrendResponse(BaseModel):
    trends: List[MarketTrendDataPoint]

# --- Product Models (SQLite) ---
class ProductBase(BaseModel):
    title: str
    millet_type: str
    product_form: str
    description: Optional[str] = None
    available_quantity_kg: float
    price_per_kg: float
    minimum_order_kg: float = 1.0
    harvest_date: Optional[str] = None
    organic_certified: bool = False
    quality_grade: Optional[str] = None
    moisture_content: Optional[float] = None
    location_state: str
    location_district: str
    seller_id: str
    certifications: Optional[Any] = None
    images: Optional[Any] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    millet_type: Optional[str] = None
    product_form: Optional[str] = None
    description: Optional[str] = None
    available_quantity_kg: Optional[float] = None
    price_per_kg: Optional[float] = None
    minimum_order_kg: Optional[float] = None
    harvest_date: Optional[str] = None
    organic_certified: Optional[bool] = None
    quality_grade: Optional[str] = None
    moisture_content: Optional[float] = None
    location_state: Optional[str] = None
    location_district: Optional[str] = None
    certifications: Optional[Any] = None
    images: Optional[Any] = None
    is_active: Optional[bool] = None


