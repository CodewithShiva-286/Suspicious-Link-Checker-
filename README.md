# Suspicious Link Checker

Service-based cybersecurity tool that analyzes submitted URLs using:
- Google Safe Browsing
- VirusTotal
- WHOIS (domain age)
- SSL certificate checks

It returns:
- Verdict (`safe`, `suspicious`, `malicious`)
- Confidence score
- Explainable reason trace
- Step-by-step scan timeline

## Project Structure

- `backend/` - FastAPI API, provider integrations, rule-based decision engine, MongoDB persistence
- `frontend/` - React UI with futuristic scan dashboard and timeline
- `docs/` - PRD and planning artifacts

## Backend Quick Start

1. Create virtual environment and install dependencies:
   - `pip install -r backend/requirements.txt`
2. Copy env:
   - `copy backend\\.env.example backend\\.env`
3. Start API:
   - `uvicorn app.main:app --reload --app-dir backend`

## Frontend Quick Start

1. Install dependencies:
   - `npm install --prefix frontend`
2. Copy env:
   - `copy frontend\\.env.example frontend\\.env`
3. Start dev server:
   - `npm run dev --prefix frontend`
