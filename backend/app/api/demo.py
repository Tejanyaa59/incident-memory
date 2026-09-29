from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.seed.seeder import seed_database
from app.services.learning_service import learning_service

router = APIRouter(prefix="/api/demo", tags=["Demo"])

@router.post("/reset")
def reset_demo(db: Session = Depends(get_db)):
    """Reset the local demo state to 10 historical incidents, 1 active INC-104, 4 patterns, and 0 corrections."""
    seed_database(db=db, force_reset=True)
    stats = learning_service.get_dashboard_stats(db)
    return {
        "success": True,
        "message": "Demo state reset successfully.",
        "stats": stats,
    }
