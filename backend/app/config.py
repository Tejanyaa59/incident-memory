import os
from pathlib import Path
from dotenv import load_dotenv

# Locate .env file in backend/
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "IncidentLens API"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'incidentlens.db'}")
    
    # Hindsight
    HINDSIGHT_BASE_URL: str = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io").rstrip("/")
    HINDSIGHT_API_KEY: str = os.getenv("HINDSIGHT_API_KEY", "")
    HINDSIGHT_BANK_ID: str = os.getenv("HINDSIGHT_BANK_ID", "incidentlens-production")
    
    # Hindsight Retain Mission
    HINDSIGHT_RETAIN_MISSION: str = (
        "Remember production incident symptoms, service context, technical causes, "
        "deployment context, investigation decisions, successful and unsuccessful resolutions, "
        "outcomes, and investigator feedback. Prioritize reusable engineering experience and "
        "causal relationships that can improve future incident investigations."
    )
    
    # LLM
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "")
    
    # CORS
    raw_origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:8080")
    FRONTEND_ORIGINS: list[str] = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

settings = Settings()
