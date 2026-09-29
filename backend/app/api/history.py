from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.incident_service import incident_service
from app.schemas.schemas import IncidentSchema

router = APIRouter(prefix="/api/history", tags=["Incidents"])

@router.get("", response_model=List[IncidentSchema])
def get_incident_history(db: Session = Depends(get_db)):
    """Return all historical / resolved incidents (10 initial, 11 after INC-104 is resolved)."""
    return incident_service.get_historical(db)
