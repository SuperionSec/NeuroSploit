# NeuroSploit Pro

NeuroSploit refactored to FastAPI + Ant Design Pro architecture.

## Project Structure

```
neurosploit-pro/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py          # JWT Authentication
│   │   │       ├── users.py         # User management
│   │   │       ├── scans.py         # Scan management
│   │   │       └── vulnerabilities.py
│   │   ├── core/
│   │   │   ├── config.py            # Settings
│   │   │   ├── database.py          # DB setup
│   │   │   └── security.py          # JWT & password
│   │   ├── models/                  # SQLAlchemy models
│   │   └── schemas/                 # Pydantic models
│   ├── .env
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Login/               # Login page
    │   │   ├── Dashboard/           # Dashboard
    │   │   ├── Scans/               # Scans page
    │   │   └── Vulnerabilities/     # Vulnerabilities page
    │   └── services/
    │       └── api.ts               # API client
    └── package.json
```

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:8000` (proxied) or `http://localhost:3000`

## First Time Setup

1. Create a user first using the API:

```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"admin123"}'
```

2. Then login using that user in the UI
