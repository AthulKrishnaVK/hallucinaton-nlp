# Hallucination Detection System

An AI-powered web application for detecting and analyzing hallucinations in Large Language Model (LLM) responses by evaluating generated claims against available evidence.

## Overview

Large Language Models can generate responses that appear convincing but contain unsupported or incorrect information. This project provides a system for analyzing an LLM-generated response, identifying potentially hallucinated claims, and presenting evidence-based analysis.

The application consists of a React frontend and a FastAPI backend, with AI-based processing handled on the server side.

## Features

* Hallucination detection in LLM-generated responses
* Claim identification and analysis
* Evidence-based verification
* AI-powered response analysis
* Interactive analysis interface
* REST API for hallucination analysis
* FastAPI Swagger documentation
* Responsive React frontend
* Separate frontend and backend deployment
* Production-ready CORS configuration

## System Architecture

```text
                         User
                          |
                          v
                 React Frontend
                     (Vercel)
                          |
                     HTTPS / API
                          |
                          v
                 FastAPI Backend
                    (Render)
                          |
                          v
                Claim Extraction
                          |
                          v
                 Evidence Retrieval
                          |
                          v
                 Claim Verification
                          |
                          v
                Hallucination Analysis
                          |
                          v
                  JSON Response
                          |
                          v
                 React Frontend
```

## Technology Stack

### Frontend

* React.js
* Vite
* JavaScript
* HTML5
* CSS3

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### AI and NLP

* Large Language Models
* Natural Language Processing
* Claim extraction
* Evidence retrieval
* Evidence-based verification

### Deployment

* GitHub
* Render
* Vercel

## Project Structure

```text
hallucination/
|
├── backend/
│   ├── app/
│   │   ├── ...
│   │   └── ...
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## Local Development

### Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file inside the backend directory and add the required API keys and configuration.

Example:

```env
API_KEY=your_api_key_here
```

Do not commit `.env` files or API keys to GitHub.

### Start the Backend

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

## API

### Analyze Response

```http
POST /api/analyze
```

The endpoint analyzes an LLM-generated response and returns the hallucination analysis.

Example:

```http
POST /api/analyze
Content-Type: application/json
```

Example request:

```json
{
  "text": "Your AI-generated response goes here."
}
```

The exact request and response schema depends on the implementation of the backend.

## Production Deployment

The application uses separate deployments for the frontend and backend.

```text
React Frontend
      |
      v
   Vercel
      |
      | HTTPS
      v
FastAPI Backend
      |
      v
   Render
```

### Backend Deployment

Create a Render Web Service connected to the GitHub repository.

Recommended configuration:

```text
Root Directory:
backend
```

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

After deployment, the FastAPI documentation can be accessed through:

```text
https://YOUR-RENDER-URL.onrender.com/docs
```

### Frontend Deployment

Deploy the `frontend` directory through Vercel.

Configuration:

```text
Root Directory:
frontend
```

Build command:

```bash
npm run build
```

Output directory:

```text
dist
```

## Connecting Vercel to Render

The frontend should use an environment variable for the backend URL.

For local development:

```env
VITE_API_URL=http://127.0.0.1:8000
```

For production:

```env
VITE_API_URL=https://YOUR-RENDER-URL.onrender.com
```

In React:

```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

API requests can then be made using:

```javascript
fetch(`${API_URL}/api/analyze`, {
    // request configuration
});
```

This prevents the production application from attempting to communicate with `localhost`.

## CORS Configuration

The FastAPI backend must allow requests from the deployed Vercel frontend.

Example:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://YOUR-VERCEL-APP.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Replace the Vercel URL with the actual production URL.

## Testing

### Backend

Open:

```text
https://YOUR-RENDER-URL.onrender.com/docs
```

Verify that the FastAPI Swagger interface loads correctly.

Then test:

```text
POST /api/analyze
```

### Frontend

Verify that:

* The Vercel application loads successfully.
* The frontend communicates with the Render backend.
* `/api/analyze` returns the expected response.
* No production requests are sent to `localhost`.
* No CORS errors appear in the browser console.

## Security

The following files and values should never be committed to GitHub:

```text
.env
API keys
Access tokens
Secret keys
Database credentials
```

Recommended `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
node_modules/
dist/
```

If a secret is accidentally pushed to GitHub, deleting the file is not sufficient. The exposed credential should be revoked or rotated.

## Future Improvements

* Improved claim extraction
* Multiple evidence sources
* Source credibility assessment
* Confidence scoring
* Advanced hallucination classification
* Citation verification
* Support for multiple LLM providers
* Analysis history
* User authentication
* Analytics dashboard
* Automated evaluation benchmarks
* Improved evidence retrieval

## Use Cases

The system can be used for:

* LLM response verification
* AI-generated content analysis
* Research assistance
* Educational applications
* Fact-checking workflows
* RAG evaluation
* LLM evaluation
* AI application development

## Project Status

Active Development

## License

This project is intended for educational and research purposes.
