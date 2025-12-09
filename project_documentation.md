# Shree Anna Connect - Project Documentation

## 1. Project Overview
**Shree Anna Connect** is an AI-powered digital marketplace designed to bridge the gap between Millet Farmers and Buyers. It leverages advanced AI to provide real-time assistance, quality assessment, price discovery, and smart matching, empowering farmers with technology.

## 2. Key Features

###  Smart Marketplace
-   **Real-time Listings**: Displays live product data fetched from a Supabase database.
-   **Filtering**: Users can filter by Millet Type (Foxtail, Ragi, Bajra), Form (Raw, Flour), and Location.
-   **Visuals**: High-quality images and badges for Organic/Premium certification.

###  AI Chatbot Assistant
-   **Government Schemes**: Specialized knowledge about Shree Anna Abhiyan, MSP, and PMMSY.
-   **Web Search**: Performs real-time Google Searches to fetch verified information from official government websites (`gov.in`).
-   **Source Citation**: Provides links to the sources used for every answer.
-   **Multi-lingual Support**: Capable of understanding and replying in simple, farmer-friendly language.

###  AI Quality Analysis
-   **Visual Inspection**: Farmers can upload photos of their millet produce.
-   **Gemini Vision**: The AI analyzes the image for grain size, color consistency, and impurities.
-   **Grading**: Automatically assigns a Quality Grade (A/B/C) and estimates moisture content.

### AI Price Prediction
-   **Market Analysis**: Suggests optimal selling prices based on millet type, quality, and location.
-   **Fair Pricing**: Helps farmers avoid distress selling by providing data-backed price recommendations.

### Smart Matching
-   **B2B Connections**: Matches farmers with potential bulk buyers based on location, quantity, and millet variety.

## 3. Technical Architecture

The project follows a **Microservices Architecture**:

*   **Frontend**: React (Vite) + Tailwind CSS + Shadcn UI
*   **Backend (AI Services)**: FastAPI (Python)
*   **AI Engine**: Google Gemini 1.5 Flash / 2.0 Flash (via Google Generative AI SDK & REST API)
*   **Database**: Supabase (PostgreSQL)

```mermaid
graph TD
    User[User (Farmer/Buyer)] -->|Interact| Frontend[React Frontend]
    Frontend -->|Fetch Products| Supabase[(Supabase DB)]
    Frontend -->|AI Requests| Backend[FastAPI AI Service]
    Backend -->|Generate Content| Gemini[Google Gemini API]
    Backend -->|Web Search| GoogleSearch[Google Search Tool]
```

## 4. Directory Structure & Code Description

### `frontend/` (React Application)

*   **`src/pages/Marketplace.tsx`**
    *   **Purpose**: The main shopping page.
    *   **Key Logic**: Uses `useQuery` to fetch `products` from Supabase. Implements client-side filtering and renders the `ProductCard` grid. Contains the "AI Smart Matching" trigger.
*   **`src/components/ai/ChatBot.tsx`**
    *   **Purpose**: The floating chat widget.
    *   **Key Logic**: Manages chat state (`messages`, `isOpen`). Sends user queries to the backend and renders the response, including clickable source links.
*   **`src/components/products/ProductForm.jsx`**
    *   **Purpose**: Form for farmers to add new products.
    *   **Key Logic**: Handles image uploads, form validation, and submits data to Supabase. Displays AI Quality Analysis results.
*   **`src/api/ai.ts`**
    *   **Purpose**: Centralized API client for AI services.
    *   **Key Logic**: Axios instance configured with `baseURL` and `API_KEY`. Defines TypeScript interfaces for all AI responses (`ChatResponse`, `PriceResponse`, etc.).

### `ai_services/` (FastAPI Microservice)

*   **`main.py`**
    *   **Purpose**: The entry point for the backend server.
    *   **Key Logic**: Defines FastAPI routes (`/chatbot`, `/quality-check-image`, `/price-gemini`). Handles CORS and API Key security (`verify_api_key`).
*   **`services.py`**
    *   **Purpose**: Business logic and AI integration.
    *   **Key Logic**:
        *   `generate_chat_response`: Detects intent (Govt Scheme vs General). Uses direct REST API calls to Gemini for web search to ensure compatibility.
        *   `analyze_quality_image`: Sends image bytes to Gemini Vision for analysis.
        *   `get_market_price`: Simulates market logic combined with AI reasoning.
*   **`models.py`**
    *   **Purpose**: Data validation schemas.
    *   **Key Logic**: Pydantic models (`ChatRequest`, `ChatResponse`) ensuring strict type safety for JSON I/O.

## 5. AI Integration Details

### Government Scheme Search
We use a **Hybrid Intent Detection** system:
1.  **Keyword Matching**: Checks for terms like "Shree Anna", "Subsidy", "Scheme".
2.  **Tool Use**: If matched, it constructs a prompt for Gemini to use the **Google Search Tool**.
3.  **Direct API**: We use a direct REST call to `generativelanguage.googleapis.com` to bypass SDK version limitations, ensuring reliable access to the latest search capabilities.

### Image Quality Check
1.  User uploads an image.
2.  Backend receives the file stream.
3.  Image is passed to **Gemini 1.5 Flash**.
4.  Prompt: *"Analyze this millet sample for quality, impurities, and moisture."*
5.  Output: Structured JSON with grade and issues.

## 6. Setup & Running

### Prerequisites
*   Node.js & npm
*   Python 3.9+
*   Supabase Account
*   Google Gemini API Key

### Running the Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

### Running the Backend
```bash
cd ai_services
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
# Runs on http://localhost:8000
```

## 7. Future Roadmap
*   **Voice Interface**: Add speech-to-text for illiterate farmers.
*   **Local LLMs**: Deploy quantized models on edge devices for offline support.
*   **Blockchain**: Traceability for organic certification.
