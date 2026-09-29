from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field

class BaseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class IncidentSchema(BaseSchema):
    id: str
    title: str
    service: str
    severity: str
    status: str
    date: str
    timestamp: str
    started_at: Optional[str] = Field(None, alias="startedAt")
    duration: Optional[str] = None
    error_rate: Optional[str] = Field(None, alias="errorRate")
    latency: Optional[str] = None
    db_connections: Optional[str] = Field(None, alias="dbConnections")
    cpu: Optional[str] = None
    recent_deployment: Optional[str] = Field(None, alias="recentDeployment")
    error: Optional[str] = None
    root_cause: str = Field(..., alias="rootCause")
    context: str
    resolution: str
    outcome: str
    reasoning: str = ""
    human_feedback: str = Field("", alias="humanFeedback")

class LearnedPatternSchema(BaseSchema):
    id: str
    signals: List[str]
    result: str
    confirmed: int
    successful: int

class MemoryMatchSchema(BaseSchema):
    incident_id: str = Field(..., alias="incidentId")
    similarity: int
    title: Optional[str] = None
    service: Optional[str] = None
    root_cause: Optional[str] = Field(None, alias="rootCause")
    resolution: Optional[str] = None
    outcome: Optional[str] = None
    date: Optional[str] = None
    error: Optional[str] = None

class InvestigationResultSchema(BaseSchema):
    incident_id: str = Field(..., alias="incidentId")
    likely_root_cause: str = Field(..., alias="likelyRootCause")
    confidence: int
    evidence: List[str]
    recommendations: List[str]
    reasoning: Optional[str] = ""

class InvestigationRunRequest(BaseSchema):
    incident_id: str = Field(..., alias="incidentId")

class InvestigationRunResponse(BaseSchema):
    incident: IncidentSchema
    investigation: InvestigationResultSchema
    confidence: int
    evidence: List[str]
    recommendations: List[str]
    recalled_memories: List[MemoryMatchSchema]
    memory_count: int
    hindsight_available: bool = True
    reflection: Optional[str] = None

class FeedbackRequest(BaseSchema):
    decision: Optional[str] = "confirm"  # "confirm" | "correct"
    type: Optional[str] = None           # frontend support: "confirmed" | "corrected"
    corrected_root_cause: Optional[str] = Field(None, alias="rootCause")
    resolution: Optional[str] = None
    outcome: Optional[str] = None
    notes: Optional[str] = ""

class FeedbackResponse(BaseSchema):
    id: int
    incident_id: str = Field(..., alias="incidentId")
    decision: str
    corrected_root_cause: Optional[str] = None
    resolution: Optional[str] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None

class DashboardStatsResponse(BaseSchema):
    active_incidents: int
    historical_incidents: int
    learned_patterns: int
    hindsight_memories: int
    confirmed_outcomes: int
    investigator_corrections: int

class MemoryPageResponse(BaseSchema):
    total_memories: int
    learned_patterns: int
    confirmed_outcomes: int
    investigator_corrections: int
    memories: List[IncidentSchema]
    patterns: List[LearnedPatternSchema]

class LearningPageResponse(BaseSchema):
    historical_incidents: int
    learned_patterns: int
    investigation_relevance: int
    recent_learning_events: List[str]
    patterns: List[LearnedPatternSchema]

class HealthResponse(BaseSchema):
    status: str
    hindsight: str
    database: str
