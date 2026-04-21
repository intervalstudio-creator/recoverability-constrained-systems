# Boundary v4.1 — Feature Modules

This document describes the six feature modules added in v4.1. Each module addresses a specific gap between where recoverability failures are detected and where they are acted on.

---

## Feature 1 — Cross-Institutional Continuity Monitor

**The gap it addresses:** Most institutional harm is invisible. A patient deteriorates across three departments and nobody sees the whole picture. A person loses housing, income, and identity in sequence and each institution sees only its own slice.

**What it does:** Evaluates a person as a continuity object across all active domains simultaneously. Produces a unified picture — per-domain states, worst combined state, cascading dependencies, and a compound non-admissibility signal.

**Compound non-admissibility:** When three or more domains are simultaneously `DEGRADED`, no single domain triggers a `NON-ADMISSIBLE` alert. But the combined picture is non-admissible. This signal would be invisible to any single institution. Boundary raises it.

**Cascading risk:** When a domain is `NON-ADMISSIBLE`, Boundary checks which dependent domains are also active and flags them as at risk. A healthcare failure automatically checks transport, finance, and identity.

**Module:** `engine/continuity_monitor.py`

**API:**
- `POST /api/monitor/subject` — evaluate a person across all active domains
- `POST /api/monitor/population` — evaluate a list of subjects simultaneously

**Input:**
```json
{
  "subject_id": "patient-001",
  "label": "Jane Smith",
  "domains": {
    "pharmacological": { "supply_days_remaining": 0, "...": "..." },
    "finance": { "bank_locked": true, "...": "..." },
    "housing": { "eviction_imminent": true, "...": "..." }
  }
}
```

---

## Feature 2 — Point-of-No-Return Clock

**The gap it addresses:** The most common failure pattern in serious incidents is not that nobody knew — it is that people knew too late. Escalation happened after the point of no return had already passed.

**What it does:** Maintains a live countdown per case before the next irreversible transition. Updates as state changes. Degrades through four thresholds. Shows the timing margins for detection, response, and recovery separately, so the operator can see not just how much time is left but whether a full recovery cycle can be completed within it.

**Thresholds:**

| Threshold | Time remaining | Signal |
|---|---|---|
| safe | > 7 days | Continue monitoring |
| monitor | ≤ 7 days | Increase monitoring |
| degraded | ≤ 24 hours | Active intervention |
| warning | ≤ 4 hours | Urgent action |
| critical | ≤ 1 hour | Escalate immediately |
| CROSSED | ≤ 0 | Point of no return passed |

**Module:** `engine/ponr_clock.py`

**API:**
- `POST /api/clock/register` — register a new clock for a case
- `POST /api/clock/update` — update seconds remaining
- `GET /api/clock/all` — all active clocks with display
- `GET /api/clock/critical` — clocks at critical or crossed threshold

---

## Feature 3 — Override Accountability Record

**The gap it addresses:** When institutions continue despite non-admissible conditions, the continuation is usually undocumented. Nobody recorded who decided to proceed, why, and when. When things go wrong, there is no trail.

**What it does:** Creates a formal, tamper-evident record of every override. All attribution fields are mandatory — the system refuses to create a record without them. Records are SHA-256 hashed for integrity. The hash is recomputed on every read; any alteration is detectable.

**Mandatory fields:**
- Operator identity
- Operator role
- Authorising authority (name + role)
- Stated reason for continuation
- Acknowledged risk and mitigations

**Integrity:** Each record contains a SHA-256 hash of its full content. If any field is modified after creation, the hash will not match on verification. The accountability report flags tampered records.

**Use cases:** Regulatory review, legal proceedings, incident investigation, institutional learning.

**Module:** `engine/override_accountability.py`

**API:**
- `POST /api/override/formal` — create a formal accountability record
- `POST /api/override/report` — generate accountability report with integrity verification
- `GET /api/override/records` — list all records

---

## Feature 4 — Plain-Language Case Builder

**The gap it addresses:** The people most affected by non-admissible continuity are usually the least able to articulate what is happening in a way institutions will act on. A person in a medication crisis, housing emergency, or bank lockout cannot write a formal recoverability evaluation. But their description of their situation contains the same information.

**What it does:** Guides a non-expert through their situation with plain-language yes/no questions. Translates their answers into a formal recoverability evaluation using the same engine as expert evaluations. Returns the result in plain language with a clear headline, explanation, and recommended action.

**The output is identical to an expert evaluation** — same four states, same rule trace, same audit record. The plain-language interface is a translation layer, not a different system.

**Result translation:**

| State | Plain headline |
|---|---|
| CONTINUE | Your situation appears manageable right now. |
| DEGRADED | Your situation is weakened. Action is needed soon. |
| NON-ADMISSIBLE | Your situation cannot continue as it is. |
| NON-EXECUTABLE | This is a crisis. You need help right now. |

**Module:** `engine/plain_language.py`

**API:**
- `GET /api/plain/domains` — list of plain-language situation types
- `GET /api/plain/questions/{domain}` — question tree for a domain
- `POST /api/plain/evaluate` — evaluate from plain-language answers

**Domains with question trees:** pharmacological, healthcare, finance, housing, identity, disaster

---

## Feature 5 — Research Corpus

**The gap it addresses:** Almost no structured data exists on how continuity failures propagate across domains. Individual cases are known but patterns are not. The incident library, used at scale, is the first dataset of its kind.

**What it does:** Treats the accumulated evaluation records as a structured research corpus. Provides anonymisation, pattern detection, statistical summaries, and export in research and regulatory formats.

**Pattern detection:**
- Most common single failure conditions
- Escalation gap rate — proportion of cases that reached `NON-EXECUTABLE`, suggesting late or absent escalation
- Domain clustering — highest non-admissible rates by domain
- Average time remaining at `NON-ADMISSIBLE` — how early are cases being detected?
- Override rate

**Anonymisation:** Identifying fields (case ID, operator ID, subject label) are replaced with pseudonymous SHA-256 hashes before research export. Structural and timing information is preserved.

**Export formats:**
- JSON (anonymised, with pattern analysis)
- CSV (flat, suitable for statistical tools)
- Regulatory submission pack (structured for patient safety, operational risk, governance submissions)

**Module:** `engine/research_corpus.py`

**API:**
- `GET /api/corpus/patterns` — detect patterns in the incident library
- `POST /api/corpus/export` — export anonymised corpus
- `POST /api/corpus/regulatory` — generate regulatory submission pack

---

## Feature 6 — Population-Level Continuity View

**The gap it addresses:** Continuity failures often happen in clusters — a care home, a ward, a refugee settlement, a disaster zone — where many people are simultaneously in non-admissible states. Evaluating one case at a time cannot see this.

**What it does:** Evaluates a cohort as a unit. Every subject is evaluated simultaneously. The output includes individual results, aggregate state counts, domain clustering signals, cascade risk, and a population-level alert.

**Systemic signals:**
- Three or more subjects failing the same domain = domain clustering = possible systemic cause rather than individual failure
- 30% or more of subjects `DEGRADED` = population degradation threshold
- Any subject `NON-EXECUTABLE` = immediate escalation regardless of overall population state

**Snapshot comparison:** Consecutive cohort evaluations can be compared to detect whether the population is `WORSENING`, `IMPROVING`, or `STABLE`.

**Deployment contexts:** hospital ward, care home, refugee settlement, disaster response zone, emergency accommodation, any defined group under shared conditions.

**Module:** `engine/population_view.py`

**API:**
- `POST /api/cohort/evaluate` — evaluate a named cohort
- `POST /api/monitor/population` — evaluate an ad-hoc list of subjects
