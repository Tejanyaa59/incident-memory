import logging
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import Incident, InvestigatorFeedback, MemoryRecord, LearnedPattern, LearningEvent
from app.hindsight.client import hindsight_service

logger = logging.getLogger("incidentlens.incident_service")

class IncidentService:
    def get_all(self, db: Session) -> List[Incident]:
        return db.query(Incident).all()

    def get_active(self, db: Session) -> List[Incident]:
        return db.query(Incident).filter(Incident.status == "Active").all()

    def get_historical(self, db: Session) -> List[Incident]:
        return db.query(Incident).filter(Incident.status == "Resolved").all()

    def get_by_id(self, db: Session, incident_id: str) -> Optional[Incident]:
        return db.query(Incident).filter(Incident.id == incident_id).first()

    def submit_feedback(
        self,
        db: Session,
        incident_id: str,
        decision: str,
        corrected_root_cause: Optional[str] = None,
        resolution: Optional[str] = None,
        outcome: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> InvestigatorFeedback:
        """Record human investigator feedback."""
        incident = self.get_by_id(db, incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")

        # Standardize decision format
        clean_decision = "correct" if decision in ["correct", "corrected"] else "confirm"

        feedback = InvestigatorFeedback(
            incident_id=incident_id,
            decision=clean_decision,
            corrected_root_cause=corrected_root_cause,
            resolution=resolution,
            outcome=outcome,
            notes=notes,
        )
        db.add(feedback)

        # Update human_feedback note on the incident
        if clean_decision == "confirm":
            note_str = f"Confirmed — {notes}" if notes else "Confirmed by incident investigator"
            incident.human_feedback = note_str
        else:
            note_str = f"Corrected — {notes or 'Investigator supplied corrected diagnosis'}"
            incident.human_feedback = note_str
            if corrected_root_cause:
                incident.root_cause = corrected_root_cause

        db.commit()
        db.refresh(feedback)
        return feedback

    def save_to_memory(
        self,
        db: Session,
        incident_id: str,
        feedback_decision: Optional[str] = None,
        corrected_root_cause: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retain confirmed incident outcome into persistent Hindsight and SQLite organizational memory (Idempotent)."""
        incident = self.get_by_id(db, incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")

        # Idempotency check: verify if already stored in memory
        existing_memory = db.query(MemoryRecord).filter(MemoryRecord.incident_id == incident_id).first()
        if existing_memory:
            logger.info(f"[MEMORY] Incident {incident_id} already saved in memory. Returning existing record (Idempotent).")
            return {
                "success": True,
                "message": f"Incident {incident_id} was already in organizational memory.",
                "incident": incident,
                "already_exists": True,
            }

        decision = feedback_decision or "confirm"
        is_confirm = decision in ["confirm", "confirmed"]

        # 1. Update incident state
        incident.status = "Resolved"
        if not incident.outcome or incident.outcome == "Pending investigator confirmation":
            incident.outcome = "Resolved in 7 minutes"
        if not incident.resolution:
            incident.resolution = "Rollback deployment"

        if is_confirm:
            incident.human_feedback = f"Confirmed{f' — {notes}' if notes else ''}"
        else:
            if corrected_root_cause:
                incident.root_cause = corrected_root_cause
            incident.human_feedback = f"Corrected — {notes or 'Investigator supplied corrected diagnosis'}"

        # 2. Retain in real Hindsight
        logger.info(f"[MEMORY] Retaining {incident_id}")
        incident_dict = {
            "id": incident.id,
            "title": incident.title,
            "service": incident.service,
            "severity": incident.severity,
            "date": incident.date,
            "error": incident.error,
            "context": incident.context,
            "root_cause": incident.root_cause,
            "resolution": incident.resolution,
            "outcome": incident.outcome,
            "human_feedback": incident.human_feedback,
            "error_rate": incident.error_rate,
            "latency": incident.latency,
            "db_connections": incident.db_connections,
            "cpu": incident.cpu,
        }
        hindsight_service.retain(incident_dict)

        # 3. Save memory record in SQLite
        mem_rec = MemoryRecord(
            incident_id=incident_id,
            hindsight_reference=f"incident-{incident_id}",
            memory_type="confirmed_incident",
            content=hindsight_service.format_incident_content(incident_dict),
        )
        db.add(mem_rec)

        # 4. Learning events and pattern reinforcement
        if is_confirm:
            ev1 = LearningEvent(
                incident_id=incident_id,
                event_type="memory_retained",
                description=f"{incident_id} added to organizational memory",
            )
            ev2 = LearningEvent(
                incident_id=incident_id,
                event_type="pattern_reinforced",
                description=f"{incident_id} reinforced the database connection leak pattern associated with recent deployments and high database connection utilization.",
            )
            db.add_all([ev1, ev2])

            # Strengthen Pattern PAT-01
            pat1 = db.query(LearnedPattern).filter(LearnedPattern.id == "PAT-01").first()
            if pat1:
                pat1.confirmed += 1
                pat1.successful += 1
        else:
            ev = LearningEvent(
                incident_id=incident_id,
                event_type="correction_learned",
                description=f"Correction learned for {incident_id}: root cause corrected to {incident.root_cause}",
            )
            db.add(ev)

        db.commit()
        db.refresh(incident)
        logger.info(f"[MEMORY] Memory saved successfully for {incident_id}")

        return {
            "success": True,
            "message": f"{incident_id} has been added to organizational memory.",
            "incident": incident,
            "already_exists": False,
        }

incident_service = IncidentService()
