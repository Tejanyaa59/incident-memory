from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.incident_service import incident_service
from app.investigation.engine import investigation_engine
from app.schemas.schemas import InvestigationRunRequest, InvestigationRunResponse

router = APIRouter(prefix="/api/investigations", tags=["Investigation"])

@router.post("/run", response_model=InvestigationRunResponse)
def run_investigation(
    payload: InvestigationRunRequest,
    db: Session = Depends(get_db),
):
    """
    Execute AI investigation combining current incident evidence,
    real Hindsight recall, deterministic reasoning, and optional LLM synthesis.
    """
    incident = incident_service.get_by_id(db, payload.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident {payload.incident_id} not found")

    result = investigation_engine.investigate(incident, db)
    return result
