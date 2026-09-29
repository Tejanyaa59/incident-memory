import { activeIncidents, historicalIncidents, investigationResult, learnedPatterns, memoryMatches } from "@/data/mockData";
import type { FeedbackInput, Incident, InvestigationResult, LearnedPattern, MemoryMatch } from "@/types/incident";

const API_BASE = (import.meta as any).env?.VITE_API_URL || "http://localhost:8000";

async function request<T>(endpoint: string, options?: RequestInit, fallback?: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
      ...options,
    });
    if (!res.ok) {
      console.warn(`API error ${res.status} on ${endpoint}`);
      if (fallback !== undefined) return fallback;
      throw new Error(`API error ${res.status}: ${res.statusText}`);
    }
    return (await res.json()) as T;
  } catch (err) {
    console.warn(`Network/API failure on ${endpoint}, falling back if available:`, err);
    if (fallback !== undefined) return fallback;
    throw err;
  }
}

export async function getIncidents(): Promise<Incident[]> {
  return request<Incident[]>("/api/incidents", undefined, [...historicalIncidents, ...activeIncidents]);
}

export async function getActiveIncidents(): Promise<Incident[]> {
  return request<Incident[]>("/api/incidents/active", undefined, activeIncidents);
}

export async function getHistoricalIncidents(): Promise<Incident[]> {
  return request<Incident[]>("/api/history", undefined, historicalIncidents);
}

export async function getIncident(id: string): Promise<Incident | undefined> {
  return request<Incident>(`/api/incidents/${id}`, undefined, [...historicalIncidents, ...activeIncidents].find((i) => i.id === id));
}

export async function getSimilarMemories(id: string): Promise<MemoryMatch[]> {
  return request<MemoryMatch[]>(`/api/incidents/${id}/memories`, undefined, id === "INC-104" ? memoryMatches : []);
}

export async function runInvestigation(id: string): Promise<InvestigationResult> {
  const data = await request<any>(
    "/api/investigations/run",
    {
      method: "POST",
      body: JSON.stringify({ incidentId: id }),
    },
    id === "INC-104" ? investigationResult : undefined
  );

  if (!data) return investigationResult;

  const inv = data.investigation || data;
  const similarMemories = data.recalled_memories
    ? data.recalled_memories.map((m: any) => ({
        incidentId: m.incidentId || m.id,
        similarity: m.similarity,
      }))
    : data.similarMemories || (id === "INC-104" ? memoryMatches : []);

  return {
    incidentId: inv.incidentId || id,
    likelyRootCause: inv.likelyRootCause || "Database connection leak following recent deployment",
    confidence: inv.confidence || data.confidence || 89,
    evidence: inv.evidence || data.evidence || [],
    recommendations: inv.recommendations || data.recommendations || [],
    similarMemories,
  };
}

export async function submitFeedback(data: FeedbackInput): Promise<any> {
  return request<any>(
    `/api/incidents/${data.incidentId}/feedback`,
    {
      method: "POST",
      body: JSON.stringify(data),
    },
    data
  );
}

export async function saveMemory(data: Incident): Promise<any> {
  return request<any>(
    `/api/incidents/${data.id}/memory`,
    {
      method: "POST",
      body: JSON.stringify(data),
    },
    data
  );
}

export async function getLearningStats(): Promise<{
  memories: number;
  patterns: number;
  confirmed: number;
  corrections: number;
}> {
  const fallback = {
    memories: historicalIncidents.length,
    patterns: learnedPatterns.length,
    confirmed: historicalIncidents.length,
    corrections: 0,
  };
  try {
    const stats = await request<{
      hindsightMemories: number;
      learnedPatterns: number;
      confirmedOutcomes: number;
      corrections: number;
    }>("/api/dashboard/stats", undefined, {
      hindsightMemories: fallback.memories,
      learnedPatterns: fallback.patterns,
      confirmedOutcomes: fallback.confirmed,
      corrections: fallback.corrections,
    });
    return {
      memories: stats.hindsightMemories,
      patterns: stats.learnedPatterns,
      confirmed: stats.confirmedOutcomes,
      corrections: stats.corrections,
    };
  } catch {
    return fallback;
  }
}

export async function getPatterns(): Promise<LearnedPattern[]> {
  try {
    const learning = await request<{ patterns: LearnedPattern[] }>("/api/learning", undefined, { patterns: learnedPatterns });
    return learning.patterns || learnedPatterns;
  } catch {
    return learnedPatterns;
  }
}

export async function getLearningData(): Promise<{
  patterns: LearnedPattern[];
  learningEvents: string[];
  stats: any;
}> {
  return request<any>("/api/learning", undefined, {
    patterns: learnedPatterns,
    learningEvents: [
      "INC-031 stored in memory — Pool exhaustion",
      "INC-052 stored in memory — Leaked connections",
      "INC-083 stored in memory — Missing close()",
      "Pattern PAT-01 formed from 3 historical incidents",
      "Investigation engine updated with connection pool rule",
    ],
    stats: {
      totalMemories: historicalIncidents.length,
      learnedPatterns: learnedPatterns.length,
      confirmedOutcomes: historicalIncidents.length,
      corrections: 0,
    },
  });
}

export async function resetDemo(): Promise<any> {
  return request<any>("/api/demo/reset", { method: "POST" });
}

export async function checkHealth(): Promise<{
  status: string;
  hindsight_available: boolean;
  hindsight_bank: string;
  llm_configured: boolean;
}> {
  return request<any>("/api/health", undefined, {
    status: "ok",
    hindsight_available: true,
    hindsight_bank: "incidentlens-production",
    llm_configured: false,
  });
}
