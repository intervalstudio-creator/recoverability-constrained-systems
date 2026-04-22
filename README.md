# Boundary Platform v4.1 — Recoverability-Constrained Execution System

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19674392.svg)](https://doi.org/10.5281/zenodo.19674392)

DOI: https://doi.org/10.5281/zenodo.19674392

Boundary evaluates recoverability and produces admissibility states.  
It does not make or enforce clinical, legal, financial, or operational decisions.  
All outputs require action by a responsible human authority.

Boundary identifies when continuation becomes non-recoverable in time under real conditions and requires visibility and escalation.

It operationalizes a universal execution constraint across human, institutional, computational, artificial intelligence, robotic, and hybrid systems.
---

## Project guidance

For current repository direction and preserved project references, read:

- [docs/RECOVS_REFERENCE_PACK.md](C:\Users\usuario\Documents\Codex\recoverability-constrained-systems\docs\RECOVS_REFERENCE_PACK.md)
- [docs/WEBSITE_DIRECTION_GAP_ANALYSIS.md](C:\Users\usuario\Documents\Codex\recoverability-constrained-systems\docs\WEBSITE_DIRECTION_GAP_ANALYSIS.md)
- [docs/IMPLEMENTATION_ROADMAP.md](C:\Users\usuario\Documents\Codex\recoverability-constrained-systems\docs\IMPLEMENTATION_ROADMAP.md)

These documents capture the reviewed RECOVS reference zip, the intended website direction, and the recommended next implementation phases.

---

## Core Principle

A system may evaluate, simulate, or recommend without restriction.

A system may only execute where recoverability can be established in time under real conditions as sufficient to prevent irreversible transition.

If recoverability cannot be established:

- continuation is non-admissible
- execution does not occur

---

## What Boundary outputs

Exactly four states. Nothing else.

| State | Meaning |
|---|---|
| `CONTINUE` | All recoverability conditions met. Execution is admissible. |
| `DEGRADED` | One or more conditions weakened. Margin reduced. Monitor and act. |
| `NON-ADMISSIBLE` | Recoverability cannot be established. Execution must not proceed. |
| `NON-EXECUTABLE` | Non-admissible and time-critical or authority unreachable. Escalate immediately. |

**Boundary evaluates recoverability and produces admissibility states. It does not make or enforce clinical, legal, financial, or operational decisions. All outputs require action by a responsible human authority.**

---

## Execution model

Execution is admissible only if all six conditions hold:

1. Recovery path exists
2. Recovery path is reachable under real conditions
3. Failure can be detected in time
4. Response can occur in time
5. Recovery can be executed in time
6. No irreversible transition occurs before recovery

If any condition fails: `NON-ADMISSIBLE`.
If the time window has collapsed or human authority is unreachable: `NON-EXECUTABLE`.
If a field is unknown: treated as unestablished recoverability — `NON-ADMISSIBLE`, not `DEGRADED`.

---

## Positioning

Boundary is a detection and escalation system.

It does NOT:
- provide medical advice
- replace clinicians, legal professionals, or any authority
- autonomously control real-world systems
- make or enforce operational decisions
- execute or trigger external actions in offline mode

It evaluates recoverability, produces admissibility states, and signals escalation. Every result requires action by a responsible human authority.

---

## Quick Start

### Windows

```
scripts\install_and_run.bat
```

### Mac / Linux

```bash
bash scripts/install_and_run.sh
```

Then open:
- `app/index.html` — full UI, works offline and online

Backend runs at:
- `http://127.0.0.1:8787`

---

## Architecture

```
boundary-v4/
├── engine/
│   ├── boundary_engine.py          Core evaluation engine
│   ├── continuity_monitor.py       Cross-institutional continuity monitor
│   ├── ponr_clock.py               Point-of-no-return clock registry
│   ├── override_accountability.py  Formal tamper-evident override records
│   ├── plain_language.py           Plain-language case builder
│   ├── research_corpus.py          Pattern detection, anonymisation, regulatory export
│   └── population_view.py          Population-level cohort evaluation
├── api/
│   └── server.py                   FastAPI REST server
├── observability/
│   └── observability.py            Decision trace, residue, audit, incident library
├── app/
│   └── index.html                  Full UI — expert, simple, and offline modes
├── docs/
│   ├── BOUNDARY_SPEC.md            Open protocol specification
│   ├── FEATURES.md                 Six feature modules
│   ├── API_REFERENCE.md            Complete API reference
│   ├── DEPLOYMENT.md               Deployment guide
│   ├── REGULATORY_MAPPINGS.md      Regulatory mapping
│   ├── PLATFORM_RECORD.md          Citable technical record
│   └── CHANGELOG.md                Version history
├── tests/
│   └── test_engine.py
├── scenarios/
│   └── example_cases.json
├── scripts/
│   ├── install_and_run.bat
│   └── install_and_run.sh
├── logs/                           Auto-created at runtime
└── requirements.txt
```

---

## Supported Domains

| Domain | Key failure conditions |
|---|---|
| `pharmacological` | Supply, prescriber, abrupt stop risk, dispensing, taper plan, interactions |
| `healthcare` | Missed appointments, diagnostics, transport, caregiver, oxygen, discharge |
| `identity` | Document availability, access recovery, payroll identity |
| `finance` | Bank lockout, essential payments, income interruption |
| `housing` | Eviction, utilities, habitability, re-entry |
| `legal` | Remedy reachability, court timing, enforcement gaps |
| `labour` | Wages, rest intervals, unsafe scheduling |
| `education` | Learning access, progression interruption |
| `infrastructure` | Power, network, control integrity, degraded mode |
| `disaster` | Evacuation window, shelter, communications |
| `transport` | Route availability, timing |
| `energy` | Supply interruption, backup source |
| `communications` | Primary and fallback channel availability |
| `food_water` | Access interruption |
| `supply_chain` | Critical supply gaps, alternate supplier |

---

## Engine Design

### The six recoverability conditions

Rules RC-001 through RC-006 are evaluated before any domain rules, for every case, in every domain:

```
RC-001  recovery_path_exists
RC-002  recovery_path_reachable
RC-003  failure_detectable_in_time
RC-004  response_possible_in_time
RC-005  recovery_executable_in_time
RC-006  no_irreversible_transition_before_recovery
```

### Layered evaluation

```
Layer 1 — Six Recoverability Conditions (RC-001 to RC-006)
Layer 2 — Execution Gate Conditions (human authority, timing window)
Layer 3 — Domain-Specific Rules
```

Critical failure at any layer → `NON-ADMISSIBLE`.
Critical failure + execution gate failure or time < 1 hour → `NON-EXECUTABLE`.
Major failures only → `DEGRADED`.
All conditions met → `CONTINUE`.

### Unknown = NON-ADMISSIBLE

An unknown field on a critical rule is unestablished recoverability. Unestablished recoverability is non-admissible.

---

## New in v4.1 — Six Feature Modules

### 1. Cross-Institutional Continuity Monitor

Evaluates a person across all active domains simultaneously. Detects when the combined picture is non-admissible even when no single institution has triggered an alert. Detects compound non-admissibility and cascading domain dependencies.

`engine/continuity_monitor.py` — `POST /api/monitor/subject`

### 2. Point-of-No-Return Clock

A live countdown per case before the next irreversible transition. Four thresholds: monitor → degraded → warning → critical → CROSSED. Shows detection, response, and recovery timing margins separately.

`engine/ponr_clock.py` — `GET /api/clock/all`, `POST /api/clock/register`

### 3. Override Accountability Record

A formal, tamper-evident record of every override. SHA-256 integrity hash. All attribution fields mandatory. Suitable for regulatory review and legal proceedings. A record without full attribution is itself a boundary violation.

`engine/override_accountability.py` — `POST /api/override/formal`

### 4. Plain-Language Case Builder

Step-by-step question flow in ordinary words. Translates answers into a formal recoverability evaluation. Returns results in plain language. Same engine, same states, same rule trace as expert evaluation.

`engine/plain_language.py` — `POST /api/plain/evaluate`

### 5. Research Corpus

The incident library as a structured dataset. Anonymisation pipeline. Pattern detection — failure conditions, escalation gap rate, domain clustering, timing. Export: JSON, CSV, regulatory packs.

`engine/research_corpus.py` — `GET /api/corpus/patterns`, `POST /api/corpus/regulatory`

### 6. Population-Level Continuity View

Evaluates a cohort simultaneously. Aggregate counts, domain clustering (3+ subjects failing the same domain = systemic signal), cascade risk, snapshot trend comparison: WORSENING / IMPROVING / STABLE.

`engine/population_view.py` — `POST /api/cohort/evaluate`

---

## API Reference

See `docs/API_REFERENCE.md` for the full reference.

### Core evaluation

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/evaluate` | Single case evaluation |
| `POST` | `/api/evaluate/batch` | Batch evaluation |
| `POST` | `/api/evaluate/paths` | Path enumeration |
| `POST` | `/api/evaluate/propagate` | Cross-domain propagation |
| `POST` | `/api/events` | Event-driven evaluation trigger |

### Monitoring and escalation

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/escalation/trigger` | Signal escalation |
| `POST` | `/api/auto/start` | Start continuous re-gating |
| `POST` | `/api/auto/stop` | Stop a gate |
| `GET` | `/api/auto/status` | Active gates |

### v4.1 Feature endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/monitor/subject` | Person across all domains |
| `POST` | `/api/monitor/population` | Population snapshot |
| `POST` | `/api/cohort/evaluate` | Named cohort evaluation |
| `GET` | `/api/clock/all` | All PNR clocks |
| `GET` | `/api/clock/critical` | Critical and crossed clocks |
| `POST` | `/api/clock/register` | Register a clock |
| `POST` | `/api/override/formal` | Create accountability record |
| `POST` | `/api/override/report` | Generate accountability report |
| `GET` | `/api/plain/domains` | Plain-language domain selector |
| `GET` | `/api/plain/questions/{domain}` | Question tree for domain |
| `POST` | `/api/plain/evaluate` | Evaluate from plain answers |
| `GET` | `/api/corpus/patterns` | Detect corpus patterns |
| `POST` | `/api/corpus/export` | Export anonymised corpus |
| `POST` | `/api/corpus/regulatory` | Regulatory submission pack |

### Observability and audit

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/observability` | Dashboard summary |
| `GET` | `/api/decisions` | Decision log |
| `GET` | `/api/residue` | Unresolved residue |
| `GET` | `/api/timeline/{case_id}` | Timeline reconstruction |
| `GET` | `/api/incidents` | Incident library |
| `POST` | `/api/incidents/save` | Save to incident library |
| `GET` | `/api/audit/export` | Full audit export |
| `GET` | `/api/health` | Health check |

---

## UI Modes

### Expert mode

Full platform interface. Evaluation with domain field builder, full rule trace, explanation panel, decision log, residue log, auto re-gating, incident library, audit export, and all six v4.1 feature panels.

### Simple mode

For non-expert users. Situation type selection → step-by-step plain-language questions → single large result display with plain-language explanation and recommended action.

### Offline mode

The full evaluation engine runs in-browser as a JavaScript mirror of the Python engine. No backend required. All four states, all six RC conditions, and all domain rules are available. Offline mode performs evaluation only — it does not execute or trigger external actions. All offline evaluations are stored in session storage for audit.

---

## Observability and Audit

Every evaluation produces:
- Full rule trace — every rule evaluated, its weight, result, and reason
- Time-to-irreversibility estimate with margin warning
- Residue record for every non-admissible result
- Override record with integrity hash for every override

The residue log accumulates all unresolved states. Nothing important is silent.

---

## Override Policy

Continuation despite `NON-ADMISSIBLE` or `NON-EXECUTABLE` requires a formal accountability record with:
- Operator identity and role
- Authorising authority
- Stated reason
- Acknowledged risk

An override without full attribution is itself a boundary violation.

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Authoritative Records

Master Index: https://doi.org/10.5281/zenodo.19583410

Execution constraint:
- Universal Constraint (Closed Form): https://doi.org/10.5281/zenodo.19670123
- Ultimate Unified Closed Form: https://doi.org/10.5281/zenodo.19671515

Pharmacological domain:
- Substance, Material, Interval Systems: https://doi.org/10.5281/zenodo.19664442
- Benzodiazepine Protocol: https://doi.org/10.5281/zenodo.19664722
- Pharmacological Systems Architecture: https://doi.org/10.5281/zenodo.19664810

---

## Important

Boundary evaluates recoverability and produces admissibility states. It does not make or enforce clinical, legal, financial, or operational decisions. All outputs require action by a responsible human authority. This build does not include live credentials and does not execute real-world actions.
