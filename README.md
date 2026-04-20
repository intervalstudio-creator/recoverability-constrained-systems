# Boundary — Recoverability Execution Platform

Boundary is an executable system that determines whether continuation is admissible under real conditions and enforces **halt, restrict, contain, or escalate** when recoverability cannot be established in time.

This repository is a **live execution platform**, not a document set.

---

## Core Principle

A system may act only while recoverability can be established in time under real conditions.

If this cannot be verified:
→ continuation is non-admissible  
→ execution does not proceed  
→ escalation or halt is triggered  

---

## What this system does

- evaluates real-world scenarios under recoverability constraints  
- runs bounded-time execution cycles  
- routes decisions through authority chains  
- triggers external actions (email, SMS, incident systems, webhooks, devices)  
- applies fallback and bypass strategies  
- maintains degraded/offline operational capability  
- tracks observability, failures, and dead-letter events  

---

## System Capabilities

### Decision Engine
- recoverability-based admissibility evaluation  
- deterministic outputs: CONTINUE / ESCALATE / RESTRICT / CONTAIN / HALT  

### Execution Layer
- real-time cycle processing  
- bounded-time enforcement logic  

### External Actuation
- email (SMTP)  
- SMS (Twilio)  
- incident systems (PagerDuty)  
- webhook triggers  
- device-level actuation  

### Observability
- channel health tracking  
- action status logging  
- dead-letter queue for failed actions  
- runtime state inspection  

### Deployment Profiles
- enterprise profile  
- NHS / healthcare profile  

### Runtime Modes
- online mode  
- degraded mode  
- offline-first operation  

---

## Repository Structure

api/                → runtime server (entry point)  
app/                → user interface  
engine/             → core logic and execution system  
integrations/       → external connectors  
configs/            → authority, fallback, continuity configs  
cases/              → real-world scenarios  
docs/               → execution + deployment documentation  
scripts/            → install and run scripts  
desktop/            → desktop app wrapper (Electron)  
.github/            → auto-build and release workflows  

---

## Quick Start

### Run locally

python -m pip install -r requirements.txt  
python api/server.py  

Open:
http://127.0.0.1:8787  

---

### First test

- load a healthcare case  
- run execution cycle  

Expected:
→ system returns HALT or ESCALATE when recoverability is not established  

---

## External Integrations Setup

Copy:

.env.example → .env  

Fill in:

- SMTP credentials (email)  
- Twilio (SMS)  
- PagerDuty (incident)  
- webhook endpoints  
- device endpoints  

If not configured:
→ actions fail safely and go to dead-letter queue  

---

## Observability

Runtime endpoint:

GET /api/observability  

Provides:
- channel health  
- last action status  
- failure tracking  

Logs:
audit/logs/  

---

## Execution Endpoint

POST /api/runtime/cycle  

Processes:
- case input  
- decision  
- actuation  
- observability update  

---

## GitHub Auto Release (Installers)

To generate installers:

git tag v3.1.0  
git push origin main --tags  

Then:
- go to Actions  
- installers will be built automatically  
- available under Releases  

---

## Important

This system:
- is executable and deployable  
- enforces recoverability constraints  
- is not a certified medical or industrial control system  

Use requires:
- correct configuration  
- appropriate oversight  
- domain-specific validation  

---

## Positioning

Boundary is not:

- a framework  
- a document repository  
- a theoretical model  

Boundary is:

→ a continuation control system  
→ a decision enforcement engine  
→ a recoverability execution platform  
