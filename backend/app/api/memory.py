from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.learning_service import learning_service
from app.schemas.schemas import MemoryPageResponse

router = APIRouter(prefix="/api/memory", tags=["Hindsight Memory"])

@router.get("", response_model=MemoryPageResponse)
def get_memory_page_data(db: Session = Depends(get_db)):
    """Return all organizational memories, patterns, and investigator statistics."""
    return learning_service.get_memory_page_data(db)
