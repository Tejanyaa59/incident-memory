# IncidentLens Backend

The FastAPI backend and Hindsight memory service for IncidentLens.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite with SQLAlchemy 2.0 ORM
- **Memory Integration**: `hindsight-client` v0.10.2 (Bank: `incidentlens-production`)
- **Validation**: Pydantic v2 schemas with camelCase aliasing
- **Testing**: Pytest & FastAPI TestClient

## 📁 Directory Structure

```
backend/
├── app/
│   ├── api/                # API Routers
│   │   ├── dashboard.py    # GET /api/dashboard/stats
│   │   ├── demo.py         # POST /api/demo/reset
│   │   ├── health.py       # GET /api/health
│   │   ├── history.py      # GET /api/history
│   │   ├── incidents.py    # Incident CRUD, feedback, and memory persistence
│   │   ├── investigations.py # POST /api/investigations/run
│   │   ├── learning.py     # GET /api/learning
│   │   └── memory.py       # GET /api/memory
│   ├── database/           # SQLite database session and engine
│   ├── hindsight/          # Real Hindsight client service wrapper
│   ├── investigation/      # Diagnosis engine and optional LLM synthesis
│   ├── models/             # SQLAlchemy ORM database models
│   ├── schemas/            # Pydantic schemas (camelCase)
│   ├── seed/               # Canonical seed data (10 historical + INC-104)
│   ├── services/           # Business logic & stats calculation
│   ├── config.py           # Configuration & environment loader
│   └── main.py             # FastAPI entrypoint and CORS middleware
├── tests/                  # Pytest test suite
│   ├── conftest.py         # In-memory test fixtures
│   ├── test_api_and_pipeline.py # 15 functional requirement tests
│   └── test_hindsight_persistence.py # Persistent memory retention test
├── .env.example            # Environment variables template
├── requirements.txt        # Dependencies
└── incidentlens.db         # Persistent SQLite database (auto-created)
```

## 🚀 Running the Backend

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env

# 3. Seed initial data
python -m app.seed

# 4. Run tests
pytest

# 5. Start development server
uvicorn app.main:app --reload --port 8000
```

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health status and Hindsight availability |
| `GET` | `/api/dashboard/stats` | Dashboard metric counts |
| `GET` | `/api/incidents` | List all incidents (`?status=Active` or `Resolved`) |
| `GET` | `/api/incidents/active` | List active incidents |
| `GET` | `/api/incidents/{id}` | Get incident details |
| `GET` | `/api/incidents/{id}/memories` | Recall similar memories for an incident |
| `POST` | `/api/incidents/{id}/feedback` | Record investigator confirmation or correction |
| `POST` | `/api/incidents/{id}/memory` | Persist incident to Hindsight memory bank |
| `POST` | `/api/investigations/run` | Execute AI investigation using Hindsight recall |
| `GET` | `/api/learning` | Get learned patterns and recent learning timeline |
| `GET` | `/api/memory` | Full memory bank view with stats |
| `GET` | `/api/history` | Historical resolved incidents with search/filter |
| `POST` | `/api/demo/reset` | Reset database and memory to initial state |
