import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { activeIncidents, historicalIncidents, initialLearningEvents, learnedPatterns } from "@/data/mockData";
import { getActiveIncidents, getHistoricalIncidents, getLearningData, submitFeedback, saveMemory, checkHealth } from "@/services/api";
import type { FeedbackInput, Incident, LearnedPattern } from "@/types/incident";

type SaveResult = "saved" | "duplicate";

interface IncidentLensState {
  active: Incident[];
  memories: Incident[];
  patterns: LearnedPattern[];
  learningEvents: string[];
  corrections: number;
  confirmedOutcomes: number;
  hindsightConnected: boolean;
  refresh: () => Promise<void>;
  saveConfirmed: (notes: string) => SaveResult;
  saveCorrection: (rootCause: string, notes: string) => SaveResult;
}

const IncidentLensContext = createContext<IncidentLensState | undefined>(undefined);

export function IncidentLensProvider({ children }: { children: ReactNode }) {
  const [active, setActive] = useState<Incident[]>(activeIncidents);
  const [memories, setMemories] = useState<Incident[]>(historicalIncidents);
  const [patterns, setPatterns] = useState<LearnedPattern[]>(learnedPatterns);
  const [learningEvents, setLearningEvents] = useState<string[]>(initialLearningEvents);
  const [corrections, setCorrections] = useState(0);
  const [confirmedOutcomes, setConfirmedOutcomes] = useState(historicalIncidents.length);
  const [hindsightConnected, setHindsightConnected] = useState(true);

  const refresh = async () => {
    try {
      const [activeData, historyData, learningData, health] = await Promise.all([
        getActiveIncidents(),
        getHistoricalIncidents(),
        getLearningData(),
        checkHealth(),
      ]);

      if (health) {
        setHindsightConnected(health.hindsight_available ?? true);
      }
      if (activeData) {
        setActive(activeData);
      }
      if (historyData && historyData.length > 0) {
        setMemories(historyData);
      }
      if (learningData?.patterns && learningData.patterns.length > 0) {
        setPatterns(learningData.patterns);
      }
      if (learningData?.learningEvents && learningData.learningEvents.length > 0) {
        setLearningEvents(learningData.learningEvents);
      }
      if (learningData?.stats) {
        setConfirmedOutcomes(learningData.stats.confirmedOutcomes ?? historyData.length);
        setCorrections(learningData.stats.corrections ?? 0);
      }
    } catch (err) {
      console.warn("Backend not reachable yet, using grounded initial state:", err);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const store = (feedback: FeedbackInput): SaveResult => {
    if (memories.some((item) => item.id === feedback.incidentId)) return "duplicate";
    const current = active.find((item) => item.id === feedback.incidentId);
    if (!current) return "duplicate";

    const saved: Incident = {
      ...current,
      status: "Resolved",
      rootCause: feedback.rootCause,
      outcome: "Resolved in 7 minutes",
      date: "Sep 29, 2026",
      humanFeedback: feedback.type === "confirmed"
        ? `Confirmed${feedback.notes ? ` — ${feedback.notes}` : ""}`
        : `Corrected — ${feedback.notes || "Investigator supplied corrected diagnosis"}`,
    };

    // Optimistically update React state immediately
    setMemories((items) => [...items, saved]);
    setActive((items) => items.filter((item) => item.id !== feedback.incidentId));
    setLearningEvents((items) => [`INC-104 added to organizational memory`, ...items]);

    if (feedback.type === "confirmed") {
      setConfirmedOutcomes((value) => value + 1);
      setPatterns((items) =>
        items.map((pattern) =>
          pattern.id === "PAT-01"
            ? { ...pattern, confirmed: pattern.confirmed + 1, successful: pattern.successful + 1 }
            : pattern
        )
      );
    } else {
      setCorrections((value) => value + 1);
    }

    // Persist to backend SQLite & Hindsight asynchronously
    submitFeedback(feedback).catch((err) => console.warn("Failed to submit feedback to backend:", err));
    saveMemory(saved).catch((err) => console.warn("Failed to persist memory to backend:", err));

    return "saved";
  };

  const value = useMemo(
    () => ({
      active,
      memories,
      patterns,
      learningEvents,
      corrections,
      confirmedOutcomes,
      hindsightConnected,
      refresh,
      saveConfirmed: (notes: string) =>
        store({ incidentId: "INC-104", type: "confirmed", rootCause: "Database connection leak", notes }),
      saveCorrection: (rootCause: string, notes: string) =>
        store({ incidentId: "INC-104", type: "corrected", rootCause, notes }),
    }),
    [active, memories, patterns, learningEvents, corrections, confirmedOutcomes, hindsightConnected]
  );

  return <IncidentLensContext.Provider value={value}>{children}</IncidentLensContext.Provider>;
}

export function useIncidentLens() {
  const context = useContext(IncidentLensContext);
  if (!context) throw new Error("useIncidentLens must be used within IncidentLensProvider");
  return context;
}
