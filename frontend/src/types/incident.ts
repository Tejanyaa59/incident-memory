export type Severity = "Critical" | "High" | "Medium";
export type IncidentStatus = "Active" | "Resolved";

export interface Incident {
  id: string;
  title: string;
  service: string;
  severity: Severity;
  status: IncidentStatus;
  date: string;
  timestamp: string;
  startedAt?: string;
  duration?: string;
  errorRate?: string;
  latency?: string;
  dbConnections?: string;
  cpu?: string;
  recentDeployment?: string;
  error?: string;
  rootCause: string;
  context: string;
  resolution: string;
  outcome: string;
  reasoning: string;
  humanFeedback: string;
}

export interface MemoryMatch { incidentId: string; similarity: number }
export interface LearnedPattern {
  id: string;
  signals: string[];
  result: string;
  confirmed: number;
  successful: number;
}
export interface InvestigationResult {
  incidentId: string;
  likelyRootCause: string;
  confidence: number;
  evidence: string[];
  recommendations: string[];
}
export interface FeedbackInput {
  incidentId: string;
  type: "confirmed" | "corrected";
  rootCause: string;
  notes: string;
}
