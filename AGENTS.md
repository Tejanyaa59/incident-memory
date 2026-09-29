# Developer & Agent Guidelines — IncidentLens

## System Architecture

IncidentLens is organized into two primary tiers:

1. **`backend/`**:
   - Python 3.10+ / FastAPI REST API on port `8000`.
   - SQLite persistent database (`incidentlens.db`) using SQLAlchemy 2.0.
   - Hindsight SDK integration (`hindsight-client`) targeting bank `incidentlens-production`.
   - Investigation engine combining grounded deterministic diagnostic rules with Hindsight semantic recall and optional LLM synthesis.
   - Idempotent seeding mechanism in `app.seed` supporting multiple safe executions.

2. **`frontend/`**:
   - TanStack Start / Vite / React 19 / Tailwind CSS v4 on port `3000` (or `5173`).
   - `src/services/api.ts` handles communication with the FastAPI backend, falling back gracefully to grounded mock constants if the backend is temporarily offline.
   - `src/context/incident-lens-context.tsx` provides application state, optimistic UI updates, and background persistence.
   - File-based routing located under `src/routes/`.

## Key Commands

- **Backend**:
  - Seed DB: `python -m app.seed` (from `backend/`)
  - Run Tests: `pytest` (from `backend/`)
  - Run Server: `uvicorn app.main:app --reload --port 8000` (from `backend/`)
- **Frontend**:
  - Run Server: `npm run dev` (from `frontend/`)
  - Build: `npm run build` (from `frontend/`)
