import logging
from sqlalchemy.orm import Session
from app.database.session import Base, engine, SessionLocal
from app.models.models import Incident, LearnedPattern, LearningEvent, MemoryRecord
from app.seed.data import HISTORICAL_INCIDENTS, ACTIVE_INCIDENT, LEARNED_PATTERNS, INITIAL_LEARNING_EVENTS
from app.hindsight.client import hindsight_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("incidentlens.seeder")

def seed_database(db: Session = None, force_reset: bool = False):
    """Idempotently seed the SQLite database and Hindsight memory bank."""
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        # Create all tables if they do not exist
        Base.metadata.create_all(bind=engine)
        logger.info("[SEED] Ensuring database tables exist...")

        if force_reset:
            logger.info("[SEED] Force resetting database...")
            db.query(MemoryRecord).delete()
            db.query(LearningEvent).delete()
            db.query(LearnedPattern).delete()
            db.query(Incident).delete()
            db.commit()

        # 1. Seed Learned Patterns (4 patterns)
        for p_data in LEARNED_PATTERNS:
            existing_p = db.query(LearnedPattern).filter(LearnedPattern.id == p_data["id"]).first()
            if not existing_p:
                p = LearnedPattern(**p_data)
                db.add(p)
            elif force_reset:
                existing_p.confirmed = p_data["confirmed"]
                existing_p.successful = p_data["successful"]
                existing_p.signals = p_data["signals"]
                existing_p.result = p_data["result"]
        db.commit()

        # 2. Seed Initial Learning Events
        current_events_count = db.query(LearningEvent).count()
        if current_events_count == 0:
            for ev_text in INITIAL_LEARNING_EVENTS:
                ev = LearningEvent(event_type="historical_learning", description=ev_text)
                db.add(ev)
            db.commit()

        # 3. Seed Historical Incidents (10 incidents)
        for inc_data in HISTORICAL_INCIDENTS:
            existing_inc = db.query(Incident).filter(Incident.id == inc_data["id"]).first()
            if not existing_inc:
                inc = Incident(**inc_data)
                db.add(inc)
                db.commit()
            
            # Idempotently track in memory_records
            existing_mem = db.query(MemoryRecord).filter(MemoryRecord.incident_id == inc_data["id"]).first()
            if not existing_mem:
                mem = MemoryRecord(
                    incident_id=inc_data["id"],
                    hindsight_reference=f"incident-{inc_data['id']}",
                    memory_type="historical_incident",
                    content=hindsight_service.format_incident_content(inc_data),
                )
                db.add(mem)
                db.commit()

        # 4. Seed Active Incident (INC-104)
        existing_active = db.query(Incident).filter(Incident.id == ACTIVE_INCIDENT["id"]).first()
        if not existing_active:
            inc_active = Incident(**ACTIVE_INCIDENT)
            db.add(inc_active)
            db.commit()
        elif force_reset:
            # If reset requested, revert INC-104 back to active state
            for k, v in ACTIVE_INCIDENT.items():
                setattr(existing_active, k, v)
            db.commit()

        # 5. Seed into Hindsight if available
        if hindsight_service.is_available():
            logger.info("[SEED] Retaining historical incidents into Hindsight...")
            hindsight_service.ensure_bank()
            for inc_data in HISTORICAL_INCIDENTS:
                hindsight_service.retain(inc_data)
        else:
            logger.info("[SEED] Hindsight is currently unavailable. Historical incidents stored in SQLite.")

        # Verification counts
        hist_count = db.query(Incident).filter(Incident.status == "Resolved").count()
        act_count = db.query(Incident).filter(Incident.status == "Active").count()
        pat_count = db.query(LearnedPattern).count()
        mem_count = db.query(MemoryRecord).count()
        logger.info(
            f"[SEED COMPLETE] Historical incidents: {hist_count}, "
            f"Active incidents: {act_count}, "
            f"Patterns: {pat_count}, "
            f"Memories: {mem_count}"
        )

    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_database()
