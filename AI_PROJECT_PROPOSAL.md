# AI-Powered Microservices for Millet Marketplace

## 1. Architecture Overview
We have designed a lightweight, scalable microservice layer using **FastAPI** and **Google Gemini API**. This layer operates independently of the main application logic, ensuring modularity and ease of deployment.

- **Frontend**: React (App44)
- **AI Backend**: FastAPI + Python 3.11 (App44/Docker)
- **AI Engine**: Google Gemini Pro (via `google-generativeai`)
- **Communication**: REST API (JSON)
- **Security**: Header-based API Key Authentication (`X-API-Key`)

## 2. API Definitions

### Base URL: 

| Endpoint | Method | Purpose | Input | Output |
| :--- | :--- | :--- | :--- | :--- |
| `/chatbot` | POST | General Assistant | `{message, context}` | `{response}` |
| `/translate` | POST | Language Translation | `{text, target_language}` | `{translated_text}` |
| `/price-gemini` | POST | Price Prediction | `{millet_type, quality, location}` | `{marketPrice, recommendedPrice}` |
| `/match` | POST | Farmer-Buyer Match | `{type, millet, quantity, location}` | `{matches: []}` |
| `/quality-check` | POST | Quality Analysis | `{description, impurities}` | `{grade, moisture, recommendation}` |

## 3. Example JSON Requests & Responses

### `/price-gemini`
**Request:**
```json
{
  "millet_type": "Bajra",
  "quality_grade": "A",
  "location": "Rajasthan"
}
```
**Response:**
```json
{
  "marketPrice": 2200,
  "recommendedPrice": 2420,
  "currency": "INR",
  "reasoning": "Base price for Bajra in Rajasthan is approx 2200/quintal. Quality A gets +10% premium."
}
```

### `/quality-check`
**Request:**
```json
{
  "millet_type": "Ragi",
  "description": "Dark brown color, small grains, slightly dusty",
  "impurities": "Some husk particles visible"
}
```
**Response:**
```json
{
  "qualityGrade": "B",
  "moistureEstimate": "11-13%",
  "cleanliness": "Medium",
  "adulterationRisk": "Low",
  "recommendation": "Perform winnowing to remove husk particles before sale."
}
```

## 4. Deployment on base44

### Prerequisites
- Docker installed locally (for testing).
- App44 account and project created.

### Steps
1.  **Prepare Directory**: Ensure `Dockerfile`, `requirements.txt`, and `main.py` are in `ai_services/`.
2.  **Build Docker Image**:
    ```bash
    docker build -t millet-ai-services .
    ```
3.  **Run Locally (Test)**:
    ```bash
    docker run -p 8000:8000 --env-file .env millet-ai-services

      ```
4.  **Environment Variables**:
    - Go to App44 Dashboard > Settings > Environment Variables.
    - Add `GEMINI_API_KEY`: (Your Google Gemini Key).
    - Add `SERVICE_API_KEY`: (A secure random string for your frontend to use).

## 5. Frontend Integration Guide (React)

Create a helper function in your frontend `api` folder:

```javascript
// src/api/ai.js
const AI_BASE_URL = "https://ai-services.app44.io";
const API_KEY = process.env.REACT_APP_AI_SERVICE_KEY;

export const checkPrice = async (milletType, quality, location) => {
  const response = await fetch(`${AI_BASE_URL}/price-gemini`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify({ millet_type: milletType, quality_grade: quality, location }),
  });
  return response.json();
};
```

## 6. SIH Validation & Justification

**"Why use Gemini API instead of training a custom model?"**

> "Honorable Judges, we chose Google's Gemini API for three strategic reasons:
> 1.  **Speed & Agility**: In a 36-hour hackathon, training a robust model from scratch is risky and time-consuming. APIs allowed us to focus on **building the actual platform logic** and user experience immediately.
> 2.  **State-of-the-Art Performance**: Gemini Pro outperforms any model we could train on limited agricultural datasets in 2 days. It gives our farmers the most accurate, world-class advice possible.
> 3.  **Real-World Viability**: This architecture mimics modern enterprise solutions where 'Foundation Models' are used as reasoning engines, reducing maintenance costs and infrastructure overhead compared to hosting custom heavy weights."


