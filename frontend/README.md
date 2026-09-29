# Incident Memory

Build a complete, polished, production-style frontend web application called:

# INCIDENTLENS

### Tagline

**Don't investigate the same incident twice.**

### Product description

IncidentLens is a Learning-First AI Incident Investigator for engineering and SRE teams.

It investigates production incidents using:

* Current incident evidence
* Historical incidents
* Previous root causes
* Previous resolutions
* Investigation outcomes
* Human investigator feedback
* Persistent Hindsight memory

The central product idea is:

**Every incident teaches IncidentLens how to investigate the next one.**

This is a hackathon prototype demonstrating an AI agent that becomes more useful because it remembers previous investigations.

============================================================

## 1. VERY IMPORTANT PROJECT REQUIREMENTS

============================================================

Build ONLY the frontend.

Do NOT build a backend.

Use:

* React
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui where useful
* Recharts for charts if needed
* Lucide icons

The frontend must work completely using realistic local mock data and local React state.

Do NOT call external APIs.

Do NOT create fake API requests that pretend to connect to Hindsight.

Instead, create a clean service abstraction that can later be connected to:

* FastAPI backend
* Hindsight
* LLM

The final application must feel like a real professional SaaS product.

It must NOT look like:

* a generic AI template
* a ChatGPT clone
* a student dashboard
* a futuristic neon AI website
* an overly animated website
* a generic admin panel

This is a serious DevOps/SRE investigation product.

============================================================

## 2. HACKATHON CORE IDEA

============================================================

The most important feature is NOT the dashboard.

The most important feature is:

# MEMORY CHANGES THE INVESTIGATION

The user should be able to demonstrate:

WITHOUT MEMORY:

A new incident is investigated with limited historical context.

↓

Generic possible causes.

↓

LOWER investigation relevance.

Then:

LOAD HISTORICAL EXPERIENCE

↓

Hindsight recalls previous incidents.

↓

The same incident is investigated again.

↓

The AI now identifies a stronger likely root cause using previous organizational experience.

↓

Human investigator confirms/corrects it.

↓

The feedback becomes a new memory.

↓

Future investigations can retrieve that memory.

The UI must make this story extremely obvious.

============================================================

## 3. TARGET CUSTOMER

============================================================

The target customers are organizations that operate production software.

Primary users:

* Site Reliability Engineers
* DevOps Engineers
* Backend Engineers
* Incident Responders
* Engineering Leads
* Incident Commanders

Typical organizations:

* SaaS companies
* Fintech companies
* E-commerce companies
* Technology companies
* Enterprises
* Startups running production systems

The product solves:

"Engineering teams repeatedly investigate similar production incidents, but useful knowledge from previous incidents is often difficult to reuse immediately."

IncidentLens turns previous incident experience into organizational memory.

============================================================

## 4. CORE LEARNING LOOP

============================================================

Represent the main product workflow visually:

NEW INCIDENT
↓
CURRENT EVIDENCE
↓
HINDSIGHT MEMORY RECALL
↓
SIMILAR HISTORICAL INCIDENTS
↓
AI INVESTIGATION
↓
LIKELY ROOT CAUSE
↓
HUMAN INVESTIGATOR
↓
CONFIRM / CORRECT
↓
MEMORY UPDATED
↓
BETTER FUTURE INVESTIGATION

This flow should appear subtly throughout the application.

============================================================

## 5. VISUAL DESIGN

============================================================

Use a premium dark B2B/SaaS interface.

Color palette:

Background:
#0B0F14

Secondary background:
#11161D

Cards:
#151B23

Borders:
#26303B

Primary:
Blue / Indigo

Success:
Green

Warning:
Amber

Critical:
Red

Primary text:
White / very light gray

Secondary text:
Muted gray

Do NOT use excessive colors.

Use color mainly for:

* severity
* status
* success
* warnings
* important actions

Typography:
Inter or equivalent modern sans-serif.

Design characteristics:

* clean
* compact
* professional
* high information density
* subtle borders
* subtle shadows
* restrained rounded corners
* excellent spacing
* clear hierarchy

Avoid:

* huge hero sections
* excessive gradients
* glowing cards
* excessive glassmorphism
* giant rounded pills
* decorative AI artwork
* unnecessary illustrations
* excessive animation

============================================================

## 6. APPLICATION LAYOUT

============================================================

Create a desktop-first application.

Layout:

LEFT SIDEBAR
+
TOP BAR
+
MAIN CONTENT

Sidebar logo:

INCIDENTLENS

Under logo:

Learning-First Incident Investigator

Navigation:

1. Command Center
2. Investigate
3. Hindsight Memory
4. Learning
5. Incident History

At bottom of sidebar:

● Hindsight Connected

Environment:
Production

Top bar:

Production
Search
Notifications
User avatar

Add a small system status:

● Systems Operational

Sidebar should collapse on smaller screens.

============================================================

## 7. ROUTES

============================================================

Create these routes:

/dashboard

/investigate

/memory

/learning

/history

Use React Router.

All navigation must work.

============================================================

## 8. CENTRALIZED DATA ARCHITECTURE

============================================================

IMPORTANT:

There must be ONE source of truth for all mock data.

Create:

src/
data/
mockData.ts

Create shared TypeScript types.

Example:

Incident
{
id
title
service
severity
status
date
startedAt
duration
errorRate
latency
dbConnections
cpu
recentDeployment
error
rootCause
context
resolution
outcome
}

Create:

historicalIncidents[]

activeIncidents[]

hindsightMemories[]

learnedPatterns[]

All pages must consume this centralized data.

DO NOT hard-code the same incident separately in different components.

============================================================

## 9. CONSISTENT DATASET

============================================================

Use exactly 10 historical incidents.

These are the historical organizational memories.

---

## INC-031

Title:
Database Connection Failure

Service:
Payment API

Severity:
Critical

Root Cause:
Database connection leak

Context:
Recent deployment

Resolution:
Rollback deployment

Outcome:
Resolved in 7 minutes

Status:
Resolved

Date:
Sep 24, 2026

Error:
Connection pool exhausted

---

## INC-047

Title:
API Latency Spike

Service:
Checkout API

Severity:
High

Root Cause:
Traffic spike

Context:
3x normal traffic

Resolution:
Scale API servers

Outcome:
Resolved in 18 minutes

Status:
Resolved

Date:
Sep 25, 2026

---

## INC-052

Title:
Database Saturation

Service:
Payment API

Severity:
Critical

Root Cause:
Database connection leak

Context:
Recent deployment

Resolution:
Rollback deployment

Outcome:
Resolved in 11 minutes

Status:
Resolved

Date:
Sep 26, 2026

Error:
Connection pool exhausted

---

## INC-062

Title:
5xx Error Spike

Service:
Order Service

Severity:
High

Root Cause:
Bad configuration

Context:
Configuration change

Resolution:
Revert configuration

Outcome:
Resolved in 9 minutes

Status:
Resolved

Date:
Sep 26, 2026

---

## INC-071

Title:
Memory Exhaustion

Service:
User Service

Severity:
High

Root Cause:
Memory leak

Context:
Long service uptime

Resolution:
Restart service

Outcome:
Resolved in 14 minutes

Status:
Resolved

Date:
Sep 27, 2026

---

## INC-078

Title:
API Degradation

Service:
Order Service

Severity:
Medium

Root Cause:
Traffic spike

Context:
Marketing campaign caused traffic surge

Resolution:
Scale service

Outcome:
Resolved in 18 minutes

Status:
Resolved

Date:
Sep 27, 2026

---

## INC-083

Title:
Database Connection Failure

Service:
Payment API

Severity:
Critical

Root Cause:
Database connection leak

Context:
Recent deployment

Resolution:
Rollback deployment

Outcome:
Resolved in 8 minutes

Status:
Resolved

Date:
Sep 28, 2026

Error:
Connection pool exhausted

---

## INC-091

Title:
Payment Errors

Service:
Payment API

Severity:
High

Root Cause:
Configuration regression

Context:
Configuration deployment

Resolution:
Revert configuration

Outcome:
Resolved in 12 minutes

Status:
Resolved

Date:
Sep 28, 2026

---

## INC-096

Title:
High CPU

Service:
Search Service

Severity:
Medium

Root Cause:
Traffic spike

Context:
Traffic surge

Resolution:
Scale service

Outcome:
Resolved in 15 minutes

Status:
Resolved

Date:
Sep 29, 2026

---

## INC-101

Title:
Memory Usage Spike

Service:
User Service

Severity:
High

Root Cause:
Memory leak

Context:
New release

Resolution:
Rollback

Outcome:
Resolved in 10 minutes

Status:
Resolved

Date:
Sep 29, 2026

============================================================

## 10. CURRENT ACTIVE INCIDENT

============================================================

Create exactly ONE active incident.

INC-104

This is NOT initially part of the historical dataset.

Title:
Database Connection Failure

Service:
Payment API

Severity:
Critical

Status:
Active

Started:
10:05 AM

Duration:
12 minutes

Error Rate:
31%

API Latency:
8.7 seconds

Database Connections:
94%

CPU:
72%

Recent Deployment:
Yes — 12 minutes ago

Error:
Connection pool exhausted

The AI's initial investigation result after memory retrieval:

Likely Root Cause:

Database connection leak following recent deployment

Confidence:

89%

============================================================

## 11. HINDSIGHT MATCHES FOR INC-104

============================================================

When investigating INC-104, Hindsight should retrieve exactly:

INC-031
96% similarity

INC-052
89% similarity

INC-083
84% similarity

These are the three strongest historical memories.

Do NOT use INC-078 as a strongest match.

INC-078 should remain a contrasting example of a traffic-spike incident.

Display:

3 relevant memories found

Then show the three memory cards.

============================================================

## 12. LEARNED PATTERNS

============================================================

Create exactly 4 learned patterns.

PATTERN 1

Deployment
+
DB connections >90%
+
Connection pool exhaustion

↓

Database connection leak

Confirmed incidents:
3

Successful resolutions:
3

PATTERN 2

Traffic spike
+
High system load

↓

Capacity issue

Confirmed incidents:
3

PATTERN 3

Configuration change
+
5xx errors

↓

Configuration regression

Confirmed incidents:
2

PATTERN 4

Memory growth
+
Long uptime / new release

↓

Memory leak

Confirmed incidents:
2

Total:

4 learned patterns

============================================================

## 13. COMMAND CENTER

============================================================

Page:

# Command Center

Subtitle:

Monitor active incidents and investigate using organizational memory.

Top statistics:

ACTIVE INCIDENTS
1

HISTORICAL INCIDENTS
10

LEARNED PATTERNS
4

HINDSIGHT MEMORIES
10

Do not use fake numbers like 48 memories.

These numbers must correspond to the actual dataset.

Below:

### Active Incidents

Show only:

INC-104

Database Connection Failure

Payment API

Critical

31% error rate

8.7 sec latency

DB connections:
94%

Recent deployment:
12 min ago

Button:

Investigate

Clicking it opens:

/investigate

============================================================

## 14. HINDSIGHT LEARNING CARD

============================================================

On the Command Center show:

# Hindsight Learning

10 historical memories

4 learned patterns

10 confirmed outcomes

0 investigator corrections

Then:

RECENT LEARNING

Deployment + DB saturation
→ Connection leak

Traffic spike + high load
→ Capacity issue

Configuration change + 5xx
→ Configuration regression

Button:

View Hindsight Memory

============================================================

## 15. INVESTIGATION PAGE

============================================================

This is the MAIN DEMO PAGE.

Route:

/investigate

Header:

# AI Investigation

Subtitle:

Investigate the incident using current evidence and organizational memory.

At top:

Incident selector

Selected:

INC-104 — Database Connection Failure

============================================================

## 16. INCIDENT SUMMARY CARD

============================================================

Show:

INC-104

Database Connection Failure

Service:
Payment API

Severity:
CRITICAL

Status:
ACTIVE

Started:
10:05 AM

Duration:
12 minutes

Metrics:

Error Rate
31%

API Latency
8.7 sec

DB Connections
94%

CPU
72%

Recent Deployment
YES — 12 minutes ago

Error:

Connection pool exhausted

Button:

# Run Investigation

============================================================

## 17. INVESTIGATION LOADING EXPERIENCE

============================================================

When the user clicks:

Run Investigation

Show a short professional sequence:

Analyzing current incident...

↓

Searching Hindsight memory...

↓

Comparing historical incidents...

↓

3 relevant memories found

↓

Investigation ready

Do not make this take longer than approximately 2 seconds.

============================================================

## 18. HINDSIGHT RECALL

============================================================

Show:

# Hindsight Recall

3 relevant memories found

Subtitle:

Previous incidents that may help explain the current incident.

Memory card 1:

INC-031

96% similarity

Database Connection Failure

Root Cause:
Database connection leak

Context:
Recent deployment

Resolution:
Rollback deployment

Outcome:
Resolved in 7 minutes

CONFIRMED

Memory card 2:

INC-052

89% similarity

Database Saturation

Root Cause:
Database connection leak

Context:
Recent deployment

Resolution:
Rollback deployment

Outcome:
Resolved in 11 minutes

CONFIRMED

Memory card 3:

INC-083

84% similarity

Database Connection Failure

Root Cause:
Database connection leak

Context:
Recent deployment

Resolution:
Rollback deployment

Outcome:
Resolved in 8 minutes

CONFIRMED

Make the similarity percentage visually prominent but not excessive.

============================================================

## 19. INVESTIGATION REPORT

============================================================

After Hindsight Recall show:

# Investigation Report

Status:
Analysis complete

Likely Root Cause:

# Database connection leak following recent deployment

Confidence:

89%

Use a horizontal confidence indicator.

Then:

### Why this conclusion?

Show:

✓ Database connections above 90%

✓ Deployment occurred shortly before incident

✓ Error matches previous incidents

✓ Three relevant historical incidents show the same pattern

✓ Previous rollback successfully resolved those incidents

Then:

### Recommended Investigation

1. Inspect the latest deployment's database connection handling.
2. Compare connection lifecycle with INC-031.
3. Check for unclosed database connections.
4. Consider rollback if the connection leak is confirmed.

Do not say the AI is certain.

Use:

Likely root cause

Evidence suggests

Recommended next step

============================================================

## 20. INVESTIGATOR FEEDBACK

============================================================

At the bottom:

# Investigator Feedback

Subtitle:

Confirm or correct the investigation. Your decision becomes future organizational memory.

Question:

Was the AI diagnosis correct?

Buttons:

[ ✓ Confirm Diagnosis ]

[ ✕ Correct Diagnosis ]

============================================================

## 21. CONFIRM DIAGNOSIS FLOW

============================================================

When:

Confirm Diagnosis

is clicked:

Show:

Root Cause:
Database connection leak

Resolution:
Rollback deployment

Outcome:
Resolved in 7 minutes

Additional Notes:
textarea

Button:

# Save to Hindsight

When clicked:

Show success state:

✓ Memory Updated

INC-104 has been added to organizational memory.

Then display:

### New Learned Pattern

Deployment
+
DB connections >90%
+
Connection pool exhaustion

↓

Database connection leak

Confirmed incidents:
4

Successful resolutions:
4

Update counters:

Hindsight Memories:
11

Confirmed Outcomes:
11

Investigator Corrections:
0

IMPORTANT:

INC-104 must only be added once.

Do not create duplicates.

============================================================

## 22. CORRECT DIAGNOSIS FLOW

============================================================

If user clicks:

Correct Diagnosis

show a correction panel.

Options:

Database connection leak

Traffic spike

Configuration regression

Memory leak

Other

Allow the user to select a corrected root cause.

Show:

Why was the AI incorrect?

textarea

Button:

Save Correction

After saving:

Investigator Corrections:
1

Store INC-104 as a corrected memory.

Show:

✓ Correction Learned

"Investigator feedback has been added to organizational memory."

============================================================

## 23. MEMORY DEMO

============================================================

Create a highly visible:

# Memory Demo

button or toggle.

This is the primary hackathon presentation feature.

The demo must show:

### STEP 1 — WITHOUT MEMORY

Display:

No historical context

Possible causes:

Database issue

Deployment issue

Traffic spike

Confidence:

52%

Message:

"Without organizational memory, the investigation has limited historical context."

Button:

# Load Historical Experience

============================================================

## 24. MEMORY DEMO — LOADING

============================================================

When clicked:

Show:

Loading historical incidents...

10 incidents loaded

↓

Analyzing previous outcomes...

↓

4 patterns identified

↓

Hindsight memory ready

Then transition to:

# WITH HINDSIGHT

Likely root cause:

Database connection leak

Confidence:

89%

Relevant memories:

3

INC-031 — 96%

INC-052 — 89%

INC-083 — 84%

Learned pattern:

Deployment
+
DB connections >90%
+
Connection pool exhaustion
↓
Connection leak

This is the main WOW moment.

============================================================

## 25. HINDSIGHT MEMORY PAGE

============================================================

Route:

/memory

Header:

# Hindsight Memory

Subtitle:

What IncidentLens remembers about your engineering organization.

Statistics:

10 Total Memories

4 Learned Patterns

10 Confirmed Outcomes

0 Investigator Corrections

Initially.

Tabs:

All Memories

Incidents

Patterns

Feedback

Show all 10 historical memories.

Each memory card:

Incident ID

Service

Symptoms

Context

Root Cause

Resolution

Outcome

Investigator confirmation

Example:

INC-031

Payment API

Connection pool exhausted

Recent deployment

Root Cause:
Database connection leak

Resolution:
Rollback deployment

Outcome:
Resolved in 7 minutes

Investigator:
Confirmed

============================================================

## 26. MEMORY DETAIL MODAL

============================================================

Clicking a memory opens a detailed modal/drawer.

Show:

Incident ID

Timestamp

Service

Severity

Symptoms

Context

Root Cause

Investigation reasoning

Resolution

Outcome

Human feedback

Then:

### Future Influence

"This memory may be retrieved when a future incident contains similar database connection symptoms following a deployment."

============================================================

## 27. LEARNED PATTERNS SECTION

============================================================

On Memory page show:

# Learned Patterns

Pattern cards.

Example:

Deployment
+
DB saturation
+
Connection pool exhaustion

↓

Database connection leak

Confirmed:
3 historical incidents

Successful:
3 resolutions

After INC-104 is saved:

Confirmed:
4 incidents

Successful:
4 resolutions

============================================================

## 28. LEARNING PAGE

============================================================

Route:

/learning

Header:

# Learning

Subtitle:

See how IncidentLens improves as organizational memory grows.

Show a timeline:

### Initial Investigation

10 historical incidents available

4 learned patterns

Demo investigation relevance:
52%

↓

### Hindsight Recall

3 highly relevant historical memories retrieved

↓

### Current Investigation

Demo investigation relevance:
89%

IMPORTANT:

Label this:

Demo investigation relevance

Do NOT call this:

ML accuracy

Do NOT claim scientific validation.

============================================================

## 29. LEARNING EVENTS

============================================================

Show:

# Recent Learning Events

Examples:

✓ Connection leak diagnosis confirmed

✓ Deployment-related pattern reinforced

✓ Traffic-spike pattern stored

✓ Configuration regression pattern stored

✓ Memory leak pattern stored

After INC-104 is saved:

✓ INC-104 added to organizational memory

============================================================

## 30. INCIDENT HISTORY PAGE

============================================================

Route:

/history

Header:

# Incident History

Subtitle:

Previous incidents and their investigation outcomes.

Initially show exactly these 10:

INC-031

INC-047

INC-052

INC-062

INC-071

INC-078

INC-083

INC-091

INC-096

INC-101

Columns:

Incident

Service

Severity

Root Cause

Resolution

Outcome

Status

Date

Add:

Search incidents...

Filters:

Severity

Service

Root Cause

Status

Date

After INC-104 is saved, add:

INC-104

to history with:

Status:
Resolved

Root Cause:
Database connection leak

Resolution:
Rollback deployment

Outcome:
Resolved in 7 minutes

============================================================

## 31. IMPORTANT DATA CONSISTENCY RULE

============================================================

There must NEVER be conflicting information for the same incident.

For example:

INC-031 must always be:

Payment API
Critical
Database connection leak
Rollback deployment
Resolved in 7 minutes

INC-052 must always be:

Payment API
Critical
Database connection leak
Rollback deployment
Resolved in 11 minutes

INC-083 must always be:

Payment API
Critical
Database connection leak
Rollback deployment
Resolved in 8 minutes

INC-078 must always be:

Order Service
Medium
Traffic spike
Scale service
Resolved in 18 minutes

INC-104 must initially be:

Payment API
Critical
Active
Database connection leak as AI's likely diagnosis

============================================================

## 32. API SERVICE ABSTRACTION

============================================================

Create:

src/services/api.ts

with mock functions:

getIncidents()

getActiveIncidents()

getHistoricalIncidents()

getIncident(id)

getSimilarMemories(id)

runInvestigation(id)

submitFeedback(data)

saveMemory(data)

getLearningStats()

getPatterns()

These functions should initially use local mock data.

The code should be structured so they can later be replaced by FastAPI/Hindsight calls.

============================================================

## 33. STATE MANAGEMENT

============================================================

Use React state/context or a simple appropriate state-management approach.

The following state must update dynamically:

* memory count
* confirmed outcome count
* investigator corrections
* saved memories
* incident status
* learning events
* learned pattern confirmation counts

Example:

Initial:

10 memories

After saving INC-104:

11 memories

Do not refresh the page to update these values.

============================================================

## 34. REUSABLE COMPONENTS

============================================================

Create reusable components:

Sidebar

Topbar

StatCard

IncidentCard

IncidentTable

SeverityBadge

StatusBadge

MemoryCard

MemoryMatchCard

InvestigationReport

ConfidenceBar

EvidenceList

FeedbackPanel

PatternCard

LearningTimeline

DemoMode

SearchFilter

Toast

MemoryUpdateAnimation

Use clean component architecture.

============================================================

## 35. RESPONSIVE DESIGN

============================================================

Desktop-first.

Must work well on:

1440px desktop

1280px laptop

1024px tablet

mobile width

Sidebar collapses on smaller screens.

Tables should become horizontally scrollable or responsive cards.

============================================================

## 36. ANIMATIONS

============================================================

Use subtle animations only.

Examples:

Hindsight Recall:

Searching memory
→
Memory cards appear one by one

Memory update:

Saving
→
Memory Updated
→
Learned Pattern

Use short animations.

Do not use flashy effects.

============================================================

## 37. EMPTY / LOADING / ERROR STATES

============================================================

Create polished states.

Loading:

"Searching Hindsight memory..."

No memory:

"No relevant historical memories found."

Error:

"Memory service unavailable. Investigation can continue using current incident evidence."

Empty history:

"No incidents match your filters."

============================================================

## 38. PRODUCT LANGUAGE

============================================================

Use:

Hindsight Memory

Hindsight Recall

Historical Memory

Learned Pattern

Organizational Memory

AI Investigation

Likely Root Cause

Evidence

Recommended Investigation

Confirmed Diagnosis

Investigator Feedback

Memory Updated

Avoid:

"AI knows the answer"

"100% accurate"

"Guaranteed root cause"

"Autonomous decision"

The system is an investigation assistant, not an unquestionable authority.

============================================================

## 39. HINDSIGHT BRANDING

============================================================

Use subtle labels:

Powered by Hindsight Memory

Hindsight Recall

Memory Updated

Learned Pattern

But:

IncidentLens = product

Hindsight = memory technology

Do not make Hindsight visually larger than IncidentLens.

============================================================

## 40. MAIN 60-SECOND DEMO

============================================================

The application must support this exact presentation:

STEP 1

Open Command Center.

Say:

"We have an active production incident."

Click:

INC-104

STEP 2

Open AI Investigation.

Show:

31% error rate

8.7 sec latency

94% database connections

Recent deployment

STEP 3

Click:

Run Investigation

STEP 4

Show:

Hindsight Recall

3 relevant memories found.

INC-031
96%

INC-052
89%

INC-083
84%

STEP 5

Show:

Likely root cause:

Database connection leak

Confidence:

89%

STEP 6

Explain:

"The agent didn't just analyze the current incident. It remembered three previous incidents with the same pattern."

STEP 7

Click:

Confirm Diagnosis

STEP 8

Save to Hindsight.

Show:

✓ Memory Updated

STEP 9

Show:

New learned pattern

Deployment
+
DB saturation
+
Connection pool exhaustion
↓
Connection leak

STEP 10

Go to Hindsight Memory.

Show INC-104 has become a new organizational memory.

This should be the strongest demo flow.

============================================================

## 41. OPTIONAL SECOND DEMO

============================================================

Allow the Memory Demo to show:

WITHOUT MEMORY

52% relevance

↓

WITH HINDSIGHT

89% relevance

Do not claim these are real ML accuracy numbers.

Clearly label them:

Demo investigation relevance

============================================================

## 42. DO NOT ADD THESE FEATURES

============================================================

Do NOT add:

Login/signup

Billing

Payments

Team management

User settings

Chat page

General-purpose chatbot

Kubernetes integration

AWS integration

Datadog integration

PagerDuty integration

Real-time server monitoring

Real production logs

Authentication

Microservices

Complex ML training

Vector database

Fake external APIs

Unnecessary analytics

Unnecessary pages

The goal is a polished hackathon prototype.

============================================================

## 43. FINAL VISUAL PRIORITY

============================================================

The UI hierarchy must prioritize:

1. Current incident
2. Hindsight Recall
3. Similar historical incidents
4. Investigation reasoning
5. Human feedback
6. Memory update
7. Learned pattern

The dashboard statistics are secondary.

============================================================

## 44. FINAL QUALITY CHECK

============================================================

Before finishing, verify:

✓ Application runs without errors

✓ All routes work

✓ Sidebar navigation works

✓ All buttons work

✓ Mock data is centralized

✓ Exactly 10 historical incidents initially

✓ Exactly 1 active incident initially

✓ INC-104 is the active incident

✓ INC-031, INC-052 and INC-083 are the strongest Hindsight matches

✓ INC-078 is a traffic-spike example

✓ No duplicate incident IDs

✓ No contradictory incident data

✓ Dashboard statistics match actual data

✓ Hindsight statistics match actual data

✓ Learning statistics match actual data

✓ Incident History matches actual data

✓ Save to Hindsight works

✓ INC-104 becomes memory #11 after saving

✓ Investigator correction works

✓ Before/After Memory Demo works

✓ Loading states work

✓ Empty states work

✓ No lorem ipsum

✓ No placeholder text

✓ No TODO text visible

✓ No broken links

✓ No fake external API calls

✓ The UI looks like a professional DevOps/SRE SaaS product

✓ The first-time user understands the product within 30 seconds

============================================================

## 45. FINAL PRODUCT MESSAGE

============================================================

The product should communicate this idea throughout the experience:

# "Every incident teaches IncidentLens how to investigate the next one."

Secondary message:

**Don't investigate the same incident twice.**

Build the complete frontend now.
Do not stop at a landing page.
Do not create only static mockups.

The application must be fully navigable and interactive using the local mock data.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/ec2ae9bd-eaf9-4eb6-b00a-bac742ebbd36).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
