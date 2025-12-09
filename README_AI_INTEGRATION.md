# Shree Anna Connect - AI Integrated Platform

This document provides instructions on how to run the fully integrated AI-enabled Millet Value Chain Platform.

## 🚀 Overview

The project has been successfully migrated.
- **Frontend**: Updated React interface is in the `SHREE_ANNA` directory.
- **Backend (AI Services)**: Python FastAPI microservices are in the `ai_services` directory.

All AI features (Chatbot, Quality Check, Price Prediction) are fully integrated.

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.9 or higher)
- **Git**

---

## 🛠️ Step-by-Step Run Instructions

Open two separate terminal windows (or tabs) to run the backend and frontend simultaneously.

### Terminal 1: Start AI Backend Services

 Navigate to the AI services directory and start the FastAPI server.

```powershell
cd ai_services
# Create virtual environment (optional but recommended)
python -m venv venv
# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the server
python main.py
```

*Expected Output:* `Application startup complete. Uvicorn running on http://0.0.0.0:8000`

### Terminal 2: Start Frontend Application

Navigate to the new frontend directory (`SHREE_ANNA`) and start the development server.

```powershell
cd SHREE_ANNA

# Install dependencies (only needs to be done once)
npm install

# Run the development server
npm run dev
```

*Expected Output:* `Local: http://localhost:8080/`

---

## ✅ Verified Features

The following AI features have been migrated and verified:

1.  **🤖 Millet Assistant Chatbot**
    *   **Location**: Available on every page (bottom-right icon).
    *   **Function**: Answers queries about millets, farming, and prices.
    *   **File**: `SHREE_ANNA/src/components/ai/ChatBot.tsx`

2.  **🔍 AI Quality Check**
    *   **Location**: "My Products" -> "Add Product" form.
    *   **Function**: Upload an image to automatically grade quality and fill description.
    *   **File**: `SHREE_ANNA/src/components/products/ProductForm.jsx`

3.  **💰 Price Prediction & Matching**
    *   **Location**: Integrated into the backend services.
    *   **File**: `SHREE_ANNA/src/api/ai.ts` (Service Wrapper)

## 🔧 Troubleshooting

- **Frontend can't connect to Backend**: Ensure the backend is running on port `8000` and the frontend `.env` file has `VITE_AI_SERVICE_URL=http://localhost:8000`.
- **"Network Error"**: Check if the Python window is still running.

---

**Developed & Maintained by Antigravity**
