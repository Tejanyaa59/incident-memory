# IncidentLens frontend

## Goal
Build the complete interactive IncidentLens hackathon prototype as a serious, compact DevOps/SRE application. It will use only local mock data and React state, with no backend or external API calls.

## What will be built
- A responsive application shell with collapsible sidebar, top status bar, search, notifications, and navigation.
- Six working entry points: `/` redirects to `/dashboard`, plus `/dashboard`, `/investigate`, `/memory`, `/learning`, and `/history`.
- Command Center with the exact active incident and dataset-derived counts.
- The main AI Investigation flow: incident evidence, sub-two-second investigation sequence, exact three Hindsight matches, report, confidence, evidence, recommendations, and confirm/correct feedback.
- The Memory Demo showing the same incident at 52% relevance without memory and 89% with Hindsight.
- Hindsight Memory with tabs, all historical memories, learned patterns, feedback, and a detailed memory drawer.
- Learning timeline and events, plus searchable/filterable incident history with polished empty states.
- Dynamic in-session updates: save INC-104 once, move it into resolved history/memory, increment counts and pattern strength, or store a correction without duplicates.

## Data and interaction model
- Define shared TypeScript types and one canonical mock dataset containing exactly 10 historical incidents, one active incident, four learned patterns, and the three specified similarity matches.
- Add a local service boundary exposing the requested incident, investigation, feedback, memory, stats, and pattern operations.
- Use a shared React context as the single interactive state owner so every page updates immediately without refresh.
- Keep all timers and writes local; no network requests, authentication, persistence, or invented integrations.

## Visual direction
- Premium dark operational console using the supplied charcoal, blue, green, amber, and red roles through semantic design tokens.
- Compact typography, restrained corners, thin borders, strong information hierarchy, and subtle status/memory animations.
- Desktop-first density with a mobile drawer, responsive grids, and horizontally scrollable history where needed.
- No landing page, decorative artwork, neon effects, oversized marketing treatment, or generic chat/admin styling.

## Technical details
- Keep the project’s TanStack Router because it is the framework’s supported router; route behavior and URLs will match the brief.
- Build shared app-shell, badge, stat, incident, memory, pattern, investigation, feedback, demo, table/filter, drawer, and toast UI pieces.
- Add route-specific metadata for every content page.
- Record the local-data/state architecture decision in `AGENTS.md` and maintain a short implementation roadmap.

## Verification
- Check dataset invariants and duplicate prevention with focused tests.
- Verify current preview diagnostics and compilation after implementation.
- Exercise the 60-second flow end-to-end in the browser, including the exact matches, confirmation save, count changes, memory #11, and updated history.
- Check all routes and sidebar navigation at desktop and mobile widths, including filters, drawer, loading, success, and empty states.
