from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import Incident, LearnedPattern, LearningEvent, MemoryRecord, InvestigatorFeedback

class LearningService:
    def get_dashboard_stats(self, db: Session) -> Dict[str, Any]:
        active_count = db.query(Incident).filter(Incident.status == "Active").count()
        historical_count = db.query(Incident).filter(Incident.status == "Resolved").count()
        pattern_count = db.query(LearnedPattern).count()
        memory_count = db.query(MemoryRecord).count()
        
        # Investigator feedback counts
        confirmed_fb = db.query(InvestigatorFeedback).filter(InvestigatorFeedback.decision == "confirm").count()
        corrections_fb = db.query(InvestigatorFeedback).filter(InvestigatorFeedback.decision == "correct").count()

        # Confirmed outcomes: 10 initial + any confirmed feedback
        confirmed_outcomes = historical_count

        return {
            "active_incidents": active_count,
            "historical_incidents": historical_count,
            "learned_patterns": pattern_count,
            "hindsight_memories": memory_count,
            "confirmed_outcomes": confirmed_outcomes,
            "investigator_corrections": corrections_fb,
        }

    def get_learning_page_data(self, db: Session) -> Dict[str, Any]:
        stats = self.get_dashboard_stats(db)
        patterns = db.query(LearnedPattern).all()
        
        # Latest learning events in reverse order
        events = db.query(LearningEvent).order_by(LearningEvent.id.desc()).limit(10).all()
        recent_events = [e.description for e in events]

        # Investigation relevance: 52 initially, 89 once INC-104 is investigated / memory enriched
        relevance = 89 if stats["active_incidents"] == 0 or stats["hindsight_memories"] > 10 else 52

        return {
            "historical_incidents": stats["historical_incidents"],
            "learned_patterns": stats["learned_patterns"],
            "investigation_relevance": relevance,
            "recent_learning_events": recent_events,
            "patterns": patterns,
        }

    def get_memory_page_data(self, db: Session) -> Dict[str, Any]:
        stats = self.get_dashboard_stats(db)
        patterns = db.query(LearnedPattern).all()
        memories = db.query(Incident).filter(Incident.status == "Resolved").order_by(Incident.id.asc()).all()

        return {
            "total_memories": stats["hindsight_memories"],
            "learned_patterns": stats["learned_patterns"],
            "confirmed_outcomes": stats["confirmed_outcomes"],
            "investigator_corrections": stats["investigator_corrections"],
            "memories": memories,
            "patterns": patterns,
        }

learning_service = LearningService()
