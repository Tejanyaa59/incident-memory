import { useEffect, useRef, useState } from "react";
import { BrainCircuit, Check, CheckCircle2, LoaderCircle, RotateCcw, Sparkles, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { activeIncidents, historicalIncidents, investigationResult as fallbackInvestigation, memoryMatches as fallbackMatches } from "@/data/mockData";
import { useIncidentLens } from "@/context/incident-lens-context";
import { runInvestigation } from "@/services/api";
import type { InvestigationResult, MemoryMatch } from "@/types/incident";
import { cn } from "@/lib/utils";
import { ConfidenceBar, Eyebrow, MemoryMatchCard, PatternCard } from "./core";

const stages = [
  "Analyzing current incident...",
  "Searching Hindsight memory...",
  "Comparing historical incidents...",
  "3 relevant memories found",
  "Investigation ready",
];

export function InvestigationWorkspace() {
  const [phase, setPhase] = useState<"idle" | "running" | "complete">("idle");
  const [stage, setStage] = useState(0);
  const [investigationData, setInvestigationData] = useState<InvestigationResult>(fallbackInvestigation);
  const [matches, setMatches] = useState<MemoryMatch[]>(fallbackMatches);
  const timer = useRef<ReturnType<typeof setInterval> | undefined>(undefined);

  useEffect(() => () => { if (timer.current) clearInterval(timer.current); }, []);

  const run = () => {
    setPhase("running");
    setStage(0);

    // Call real investigation API
    runInvestigation("INC-104")
      .then((res) => {
        if (res) {
          setInvestigationData(res);
          if (res.similarMemories && res.similarMemories.length > 0) {
            setMatches(res.similarMemories);
          }
        }
      })
      .catch((err) => {
        console.warn("Investigation API fallback:", err);
      });

    timer.current = setInterval(() => {
      setStage((value) => {
        if (value >= stages.length - 1) {
          if (timer.current) clearInterval(timer.current);
          setTimeout(() => setPhase("complete"), 220);
          return value;
        }
        return value + 1;
      });
    }, 320);
  };

  if (phase === "idle") {
    return (
      <div className="panel p-6">
        <div className="flex flex-col items-center py-10 text-center">
          <div className="flex size-12 items-center justify-center rounded border border-primary/30 bg-primary/10 text-primary">
            <BrainCircuit className="size-6" />
          </div>
          <h2 className="mt-4 text-lg font-semibold">Ready to investigate</h2>
          <p className="mt-2 max-w-md text-sm text-muted-foreground">
            Analyze current evidence and recall relevant organizational memory for INC-104.
          </p>
          <Button className="mt-6" onClick={run}>
            <Sparkles />Run Investigation
          </Button>
        </div>
      </div>
    );
  }

  if (phase === "running") {
    return (
      <div className="panel overflow-hidden p-6">
        <div className="relative h-1 overflow-hidden bg-muted">
          <div className="scan-line absolute h-full w-1/3 bg-primary" />
        </div>
        <div className="mx-auto max-w-md py-10">
          <div className="mb-6 flex items-center gap-3">
            <LoaderCircle className="size-5 animate-spin text-primary" />
            <div>
              <Eyebrow>AI Investigation</Eyebrow>
              <p className="mt-1 font-medium">{stages[stage]}</p>
            </div>
          </div>
          <div className="space-y-3">
            {stages.map((item, index) => (
              <div
                key={item}
                className={cn(
                  "flex items-center gap-3 text-sm transition-opacity",
                  index <= stage ? "opacity-100" : "opacity-30"
                )}
              >
                <span
                  className={cn(
                    "flex size-5 items-center justify-center rounded-full border",
                    index < stage
                      ? "border-success bg-success/10 text-success"
                      : "border-border"
                  )}
                >
                  {index < stage && <Check className="size-3" />}
                </span>
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <InvestigationResults
      investigation={investigationData}
      matches={matches}
      onRerun={run}
    />
  );
}

function InvestigationResults({
  investigation,
  matches,
  onRerun,
}: {
  investigation: InvestigationResult;
  matches: MemoryMatch[];
  onRerun: () => void;
}) {
  const { memories } = useIncidentLens();

  return (
    <div className="space-y-6">
      <section>
        <div className="mb-3 flex items-end justify-between">
          <div>
            <div className="flex items-center gap-2">
              <BrainCircuit className="size-5 text-primary" />
              <h2 className="text-lg font-semibold">Hindsight Recall</h2>
            </div>
            <p className="mt-1 text-sm text-muted-foreground">
              Previous incidents that may help explain the current incident.
            </p>
          </div>
          <span className="text-xs font-medium text-success">
            {matches.length} relevant memories found
          </span>
        </div>
        <div className="grid gap-3 lg:grid-cols-3">
          {matches.map((match, index) => {
            const incident =
              memories.find((item) => item.id === match.incidentId) ||
              historicalIncidents.find((item) => item.id === match.incidentId);
            return incident ? (
              <MemoryMatchCard
                key={match.incidentId}
                incident={incident}
                similarity={match.similarity}
                delay={index * 110}
              />
            ) : null;
          })}
        </div>
      </section>
      <InvestigationReport investigation={investigation} onRerun={onRerun} />
      <FeedbackPanel />
    </div>
  );
}

function InvestigationReport({
  investigation,
  onRerun,
}: {
  investigation: InvestigationResult;
  onRerun: () => void;
}) {
  return (
    <section className="panel overflow-hidden">
      <div className="flex items-center justify-between border-b border-border p-5">
        <div>
          <Eyebrow>Investigation Report</Eyebrow>
          <div className="mt-2 flex items-center gap-2 text-sm text-success">
            <CheckCircle2 className="size-4" />
            Analysis complete
          </div>
        </div>
        <Button variant="ghost" size="sm" onClick={onRerun}>
          <RotateCcw />
          Rerun
        </Button>
      </div>
      <div className="grid lg:grid-cols-[1fr_0.9fr]">
        <div className="border-b border-border p-5 lg:border-b-0 lg:border-r">
          <Eyebrow>Likely Root Cause</Eyebrow>
          <h2 className="mt-3 max-w-2xl text-xl font-semibold leading-snug">
            {investigation.likelyRootCause}
          </h2>
          <p className="mt-2 text-sm text-muted-foreground">
            Evidence suggests a repeat of a known deployment-related connection pattern.
          </p>
          <div className="mt-6">
            <ConfidenceBar value={investigation.confidence} />
          </div>
          <h3 className="mt-7 text-sm font-semibold">Why this conclusion?</h3>
          <ul className="mt-3 space-y-2">
            {investigation.evidence.map((item) => (
              <li key={item} className="flex gap-2 text-sm text-muted-foreground">
                <Check className="mt-0.5 size-4 shrink-0 text-success" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="p-5">
          <Eyebrow>Recommended Investigation</Eyebrow>
          <ol className="mt-4 space-y-4">
            {investigation.recommendations.map((item, index) => (
              <li key={item} className="flex gap-3 text-sm">
                <span className="flex size-6 shrink-0 items-center justify-center rounded border border-border bg-secondary font-mono text-xs text-primary">
                  {index + 1}
                </span>
                <span className="pt-0.5 text-muted-foreground">{item}</span>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </section>
  );
}

function FeedbackPanel() {
  const { saveConfirmed, saveCorrection, patterns, memories, corrections } = useIncidentLens();
  const [mode, setMode] = useState<"choose" | "confirm" | "correct" | "saved" | "corrected">("choose");
  const [notes, setNotes] = useState("");
  const [cause, setCause] = useState("Database connection leak");

  const save = (corrected = false) => {
    const result = corrected ? saveCorrection(cause, notes) : saveConfirmed(notes);
    setMode(corrected ? "corrected" : "saved");
    if (result === "duplicate") setMode(corrected ? "corrected" : "saved");
  };

  if (mode === "saved" || mode === "corrected") {
    return (
      <section className="panel border-success/40 bg-success/5 p-6">
        <div className="flex gap-4">
          <div className="flex size-10 shrink-0 items-center justify-center rounded bg-success/15 text-success">
            <CheckCircle2 />
          </div>
          <div className="flex-1">
            <Eyebrow>{mode === "saved" ? "Memory Updated" : "Correction Learned"}</Eyebrow>
            <h2 className="mt-2 text-lg font-semibold">
              {mode === "saved"
                ? "INC-104 has been added to organizational memory."
                : "Investigator feedback has been added to organizational memory."}
            </h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Future investigations can now retrieve this confirmed outcome.
            </p>
            {mode === "saved" && (
              <div className="mt-5 max-w-md">
                {patterns[0] && <PatternCard pattern={patterns[0]} featured />}
              </div>
            )}
            <div className="mt-5 flex gap-5 text-xs text-muted-foreground">
              <span>
                <b className="text-foreground">{memories.length}</b> memories
              </span>
              <span>
                <b className="text-foreground">{corrections}</b> corrections
              </span>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="panel p-5">
      <Eyebrow>Investigator Feedback</Eyebrow>
      <h2 className="mt-2 text-lg font-semibold">Was the AI diagnosis correct?</h2>
      <p className="mt-1 text-sm text-muted-foreground">
        Confirm or correct the investigation. Your decision becomes future organizational memory.
      </p>
      {mode === "choose" ? (
        <div className="mt-5 flex flex-wrap gap-3">
          <Button onClick={() => setMode("confirm")}>
            <Check />
            Confirm Diagnosis
          </Button>
          <Button variant="outline" onClick={() => setMode("correct")}>
            <X />
            Correct Diagnosis
          </Button>
        </div>
      ) : (
        <div className="mt-5 max-w-2xl space-y-4 border-t border-border pt-5">
          {mode === "confirm" ? (
            <div className="grid gap-3 text-sm sm:grid-cols-3">
              <p>
                <span className="block text-xs text-muted-foreground">Root Cause</span>Database connection leak
              </p>
              <p>
                <span className="block text-xs text-muted-foreground">Resolution</span>Rollback deployment
              </p>
              <p>
                <span className="block text-xs text-muted-foreground">Outcome</span>Resolved in 7 minutes
              </p>
            </div>
          ) : (
            <div>
              <label className="mb-2 block text-xs text-muted-foreground">Corrected root cause</label>
              <Select value={cause} onValueChange={setCause}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {["Database connection leak", "Traffic spike", "Configuration regression", "Memory leak", "Other"].map(
                    (item) => (
                      <SelectItem key={item} value={item}>
                        {item}
                      </SelectItem>
                    )
                  )}
                </SelectContent>
              </Select>
            </div>
          )}
          <div>
            <label className="mb-2 block text-xs text-muted-foreground">
              {mode === "confirm" ? "Additional Notes" : "Why was the AI incorrect?"}
            </label>
            <Textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder={mode === "confirm" ? "Add optional investigation notes" : "Describe the corrected evidence"}
            />
          </div>
          <div className="flex gap-2">
            <Button onClick={() => save(mode === "correct")}>
              {mode === "confirm" ? "Save to Hindsight" : "Save Correction"}
            </Button>
            <Button variant="ghost" onClick={() => setMode("choose")}>
              Cancel
            </Button>
          </div>
        </div>
      )}
    </section>
  );
}

export function IncidentSelector() {
  return (
    <Select defaultValue="INC-104">
      <SelectTrigger className="w-full bg-secondary sm:w-80">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="INC-104">INC-104 — Database Connection Failure</SelectItem>
      </SelectContent>
    </Select>
  );
}

export function ActiveIncidentEvidence() {
  const { active } = useIncidentLens();
  const incident = active[0] || activeIncidents[0];
  if (!incident) return null;
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
      {[
        ["Error Rate", incident.errorRate],
        ["API Latency", incident.latency],
        ["DB Connections", incident.dbConnections],
        ["CPU", incident.cpu],
        ["Recent Deployment", "12 min ago"],
      ].map(([label, value]) => (
        <div key={label} className="panel p-4">
          <p className="text-[10px] uppercase text-muted-foreground">{label}</p>
          <p
            className={cn(
              "mt-2 text-lg font-semibold",
              (label === "Error Rate" || label === "DB Connections") && "text-critical",
              label === "Recent Deployment" && "text-warning"
            )}
          >
            {value}
          </p>
        </div>
      ))}
    </div>
  );
}
