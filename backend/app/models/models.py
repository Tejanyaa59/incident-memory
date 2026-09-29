from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

def utc_now():
    return datetime.now(timezone.utc)

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    service = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # "Critical", "High", "Medium"
    status = Column(String, nullable=False)    # "Active", "Resolved"
    date = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)
    started_at = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    error_rate = Column(String, nullable=True)
    latency = Column(String, nullable=True)
    db_connections = Column(String, nullable=True)
    cpu = Column(String, nullable=True)
    recent_deployment = Column(String, nullable=True)
    error = Column(String, nullable=True)
    root_cause = Column(String, nullable=False)
    context = Column(String, nullable=False)
    resolution = Column(String, nullable=False)
    outcome = Column(String, nullable=False)
    reasoning = Column(Text, nullable=False, default="")
    human_feedback = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=utc_now)

    investigations = relationship("Investigation", back_populates="incident", cascade="all, delete-orphan")
    feedback = relationship("InvestigatorFeedback", back_populates="incident", cascade="all, delete-orphan")
    memory_record = relationship("MemoryRecord", back_populates="incident", uselist=False, cascade="all, delete-orphan")

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False, index=True)
    likely_root_cause = Column(String, nullable=False)
    confidence = Column(Integer, nullable=False)
    reasoning = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=False, default=list)
    recommendations = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=utc_now)

    incident = relationship("Incident", back_populates="investigations")

class InvestigatorFeedback(Base):
    __tablename__ = "investigator_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False, index=True)
    decision = Column(String, nullable=False)  # "confirm" | "correct"
    corrected_root_cause = Column(String, nullable=True)
    resolution = Column(String, nullable=True)
    outcome = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    incident = relationship("Incident", back_populates="feedback")

class LearningEvent(Base):
    __tablename__ = "learning_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String, nullable=True, index=True)
    event_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)

class LearnedPattern(Base):
    __tablename__ = "learned_patterns"

    id = Column(String, primary_key=True, index=True)  # e.g., "PAT-01"
    signals = Column(JSON, nullable=False, default=list)
    result = Column(String, nullable=False)
    confirmed = Column(Integer, nullable=False, default=0)
    successful = Column(Integer, nullable=False, default=0)

class MemoryRecord(Base):
    __tablename__ = "memory_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String, ForeignKey("incidents.id"), unique=True, nullable=False, index=True)
    hindsight_reference = Column(String, nullable=True)
    memory_type = Column(String, nullable=False, default="incident_experience")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    incident = relationship("Incident", back_populates="memory_record")
