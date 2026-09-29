from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db
from app.hindsight.client import hindsight_service
from app.schemas.schemas import HealthResponse

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Health endpoint verifying database and Hindsight connectivity."""
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    hindsight_status = "connected" if hindsight_service.is_available() else "unavailable"
    overall = "ok" if (db_status == "connected" and hindsight_status == "connected") else "degraded"

    return {
        "status": overall,
        "hindsight": hindsight_status,
        "database": db_status,
    }
