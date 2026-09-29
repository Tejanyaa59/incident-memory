from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.learning_service import learning_service
from app.schemas.schemas import LearningPageResponse

router = APIRouter(prefix="/api/learning", tags=["Learning"])

@router.get("", response_model=LearningPageResponse)
def get_learning_page_data(db: Session = Depends(get_db)):
    """Return learning progression, patterns, relevance score, and learning events."""
    return learning_service.get_learning_page_data(db)
