import type { Incident, InvestigationResult, LearnedPattern, MemoryMatch } from "@/types/incident";

const base = (incident: Omit<Incident, "timestamp" | "reasoning" | "humanFeedback">): Incident => ({
  ...incident,
  timestamp: `${incident.date}, 14:30 UTC`,
  reasoning: `Current symptoms and operational context were compared with prior ${incident.service} incidents.`,
  humanFeedback: "Confirmed by incident investigator",
});

export const historicalIncidents: Incident[] = [
  base({ id:"INC-031", title:"Database Connection Failure", service:"Payment API", severity:"Critical", rootCause:"Database connection leak", context:"Recent deployment", resolution:"Rollback deployment", outcome:"Resolved in 7 minutes", status:"Resolved", date:"Sep 24, 2026", error:"Connection pool exhausted" }),
  base({ id:"INC-047", title:"API Latency Spike", service:"Checkout API", severity:"High", rootCause:"Traffic spike", context:"3x normal traffic", resolution:"Scale API servers", outcome:"Resolved in 18 minutes", status:"Resolved", date:"Sep 25, 2026" }),
  base({ id:"INC-052", title:"Database Saturation", service:"Payment API", severity:"Critical", rootCause:"Database connection leak", context:"Recent deployment", resolution:"Rollback deployment", outcome:"Resolved in 11 minutes", status:"Resolved", date:"Sep 26, 2026", error:"Connection pool exhausted" }),
  base({ id:"INC-062", title:"5xx Error Spike", service:"Order Service", severity:"High", rootCause:"Bad configuration", context:"Configuration change", resolution:"Revert configuration", outcome:"Resolved in 9 minutes", status:"Resolved", date:"Sep 26, 2026", error:"5xx errors" }),
  base({ id:"INC-071", title:"Memory Exhaustion", service:"User Service", severity:"High", rootCause:"Memory leak", context:"Long service uptime", resolution:"Restart service", outcome:"Resolved in 14 minutes", status:"Resolved", date:"Sep 27, 2026", error:"Memory growth" }),
  base({ id:"INC-078", title:"API Degradation", service:"Order Service", severity:"Medium", rootCause:"Traffic spike", context:"Marketing campaign caused traffic surge", resolution:"Scale service", outcome:"Resolved in 18 minutes", status:"Resolved", date:"Sep 27, 2026" }),
  base({ id:"INC-083", title:"Database Connection Failure", service:"Payment API", severity:"Critical", rootCause:"Database connection leak", context:"Recent deployment", resolution:"Rollback deployment", outcome:"Resolved in 8 minutes", status:"Resolved", date:"Sep 28, 2026", error:"Connection pool exhausted" }),
  base({ id:"INC-091", title:"Payment Errors", service:"Payment API", severity:"High", rootCause:"Configuration regression", context:"Configuration deployment", resolution:"Revert configuration", outcome:"Resolved in 12 minutes", status:"Resolved", date:"Sep 28, 2026", error:"Payment request errors" }),
  base({ id:"INC-096", title:"High CPU", service:"Search Service", severity:"Medium", rootCause:"Traffic spike", context:"Traffic surge", resolution:"Scale service", outcome:"Resolved in 15 minutes", status:"Resolved", date:"Sep 29, 2026", error:"CPU saturation" }),
  base({ id:"INC-101", title:"Memory Usage Spike", service:"User Service", severity:"High", rootCause:"Memory leak", context:"New release", resolution:"Rollback", outcome:"Resolved in 10 minutes", status:"Resolved", date:"Sep 29, 2026", error:"Memory usage growth" }),
];

export const activeIncidents: Incident[] = [base({
  id:"INC-104", title:"Database Connection Failure", service:"Payment API", severity:"Critical", status:"Active", date:"Sep 29, 2026", startedAt:"10:05 AM", duration:"12 minutes", errorRate:"31%", latency:"8.7 sec", dbConnections:"94%", cpu:"72%", recentDeployment:"Yes — 12 minutes ago", error:"Connection pool exhausted", rootCause:"Database connection leak", context:"Recent deployment", resolution:"Rollback deployment", outcome:"Pending investigator confirmation"
})];

export const hindsightMemories = historicalIncidents;
export const memoryMatches: MemoryMatch[] = [
  { incidentId:"INC-031", similarity:96 },
  { incidentId:"INC-052", similarity:89 },
  { incidentId:"INC-083", similarity:84 },
];
export const learnedPatterns: LearnedPattern[] = [
  { id:"PAT-01", signals:["Deployment","DB connections >90%","Connection pool exhaustion"], result:"Database connection leak", confirmed:3, successful:3 },
  { id:"PAT-02", signals:["Traffic spike","High system load"], result:"Capacity issue", confirmed:3, successful:3 },
  { id:"PAT-03", signals:["Configuration change","5xx errors"], result:"Configuration regression", confirmed:2, successful:2 },
  { id:"PAT-04", signals:["Memory growth","Long uptime / new release"], result:"Memory leak", confirmed:2, successful:2 },
];
export const investigationResult: InvestigationResult = {
  incidentId:"INC-104", likelyRootCause:"Database connection leak following recent deployment", confidence:89,
  evidence:["Database connections above 90%","Deployment occurred shortly before incident","Error matches previous incidents","Three relevant historical incidents show the same pattern","Previous rollback successfully resolved those incidents"],
  recommendations:["Inspect the latest deployment's database connection handling.","Compare connection lifecycle with INC-031.","Check for unclosed database connections.","Consider rollback if the connection leak is confirmed."],
};
export const initialLearningEvents = ["Connection leak diagnosis confirmed","Deployment-related pattern reinforced","Traffic-spike pattern stored","Configuration regression pattern stored","Memory leak pattern stored"];
