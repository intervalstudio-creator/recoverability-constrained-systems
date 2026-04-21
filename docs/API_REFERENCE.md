# Boundary API Reference v4.1

Base URL: `http://127.0.0.1:8787`

All requests and responses use `application/json`. All timestamps are ISO 8601 UTC.

---

## Core Evaluation

### POST /api/evaluate

Evaluate a single case.

**Request:**
```json
{
  "domain": "pharmacological",
  "label": "Benzo continuity check",
  "case_id": "optional-uuid",
  "operator_id": "operator@system",
  "state": {
    "recovery_path_exists": true,
    "recovery_path_reachable": true,
    "failure_detectable_in_time": true,
    "response_possible_in_time": true,
    "recovery_executable_in_time": true,
    "no_irreversible_transition_before_recovery": true,
    "human_authority_reachable": true,
    "time_remaining_seconds": 86400,
    "fallback_path_available": true,
    "supply_days_remaining": 7,
    "prescriber_reachable": true,
    "abrupt_stop_risk": false
  }
}
```

**Response:**
```json
{
  "eval_id": "uuid",
  "case_id": "uuid",
  "boundary_state": "CONTINUE",
  "failed_conditions": [],
  "unknown_fields": [],
  "time_to_irreversibility": {
    "seconds_remaining": 86400,
    "hours_remaining": 24.0,
    "point_of_no_return_crossed": false,
    "margin_warning": false
  },
  "rule_trace": [...],
  "passed_count": 12,
  "failed_count": 0,
  "unknown_count": 0,
  "total_rules_evaluated": 12,
  "timestamp": "2026-04-20T12:00:00Z"
}
```

---

### POST /api/evaluate/batch

Evaluate multiple cases simultaneously.

**Request:**
```json
{
  "cases": [
    { "domain": "pharmacological", "state": {...} },
    { "domain": "finance", "state": {...} }
  ]
}
```

**Response:**
```json
{
  "results": [...],
  "total": 2
}
```

---

### POST /api/evaluate/paths

Enumerate multiple paths for a case and check admissibility of each.

**Request:**
```json
{
  "domain": "pharmacological",
  "label": "Benzo with paths",
  "state": { "...base state..." },
  "paths": {
    "primary": { "dispensing_accessible": true },
    "fallback": { "dispensing_accessible": false, "prescriber_reachable": true },
    "emergency": { "human_authority_reachable": false }
  }
}
```

**Response:**
```json
{
  "case_id": "uuid",
  "paths_evaluated": {
    "primary": { "boundary_state": "CONTINUE", "..." },
    "fallback": { "boundary_state": "DEGRADED", "..." },
    "emergency": { "boundary_state": "NON-EXECUTABLE", "..." }
  },
  "admissible_paths": ["primary"],
  "non_admissible_paths": ["emergency"]
}
```

---

### POST /api/evaluate/propagate

Evaluate a primary case and automatically propagate to dependent domains.

**Request:**
```json
{
  "primary_case": { "domain": "healthcare", "state": {...} },
  "all_states": {
    "transport": { "route_blocked": true, "..." },
    "finance": { "bank_locked": false, "..." }
  }
}
```

**Response:**
```json
{
  "primary_domain": "healthcare",
  "primary_state": "NON-ADMISSIBLE",
  "propagated_evaluations": {
    "transport": { "boundary_state": "NON-ADMISSIBLE", "..." },
    "finance": { "boundary_state": "CONTINUE", "..." }
  },
  "cascading_non_admissible": ["transport"]
}
```

---

### POST /api/events

Event-driven evaluation trigger. Use when telemetry changes, alerts arrive, or thresholds collapse.

**Request:**
```json
{
  "event_type": "supply_threshold_crossed",
  "domain": "pharmacological",
  "case_id": "optional",
  "state": { "..." },
  "operator_id": "system"
}
```

---

## Escalation

### POST /api/escalation/trigger

Trigger a formal escalation. Creates a residue record that persists until resolved.

**Request:**
```json
{
  "case_id": "uuid",
  "domain": "pharmacological",
  "reason": "Supply failed, prescriber unreachable",
  "operator_id": "duty-manager",
  "contact_method": "phone"
}
```

**Response:**
```json
{
  "escalation_id": "uuid",
  "status": "ESCALATION_LOGGED",
  "message": "Escalation logged. A responsible human authority must be reached.",
  "timestamp": "..."
}
```

---

## Continuous Re-gating

### POST /api/auto/start

Start continuous re-evaluation of a case at a set interval.

**Request:**
```json
{
  "case": { "domain": "pharmacological", "label": "...", "state": {...} },
  "interval_seconds": 30
}
```

### POST /api/auto/stop

Stop a gate by ID: `POST /api/auto/stop?gate_id=uuid`

### GET /api/auto/status

Returns active gate IDs and count.

---

## Override

### POST /api/override

Simple override log (lightweight, for rapid logging).

**Request:**
```json
{
  "case_id": "uuid",
  "operator_id": "operator",
  "reason": "Clinical judgment override",
  "original_state": "NON-ADMISSIBLE"
}
```

### POST /api/override/formal

Create a formal, tamper-evident accountability record. All fields mandatory.

**Request:**
```json
{
  "case_id": "uuid",
  "domain": "pharmacological",
  "boundary_state": "NON-ADMISSIBLE",
  "operator_id": "dr.smith@hospital.nhs.uk",
  "operator_role": "Consultant Psychiatrist",
  "reason": "Patient requires continuation pending emergency prescription",
  "acknowledged_risk": "Withdrawal risk accepted. Patient under direct observation.",
  "authorising_authority": "Dr. J. Smith, Consultant, Ward 7B"
}
```

**Response:** Full record with `record_id` and `integrity_hash`.

### POST /api/override/report

Generate accountability report. Verifies integrity of all records.

**Request:**
```json
{
  "case_id": "optional",
  "domain": "optional",
  "from_date": "optional ISO 8601",
  "to_date": "optional ISO 8601"
}
```

### GET /api/override/records

List all override records. Optional `?domain=` filter.

---

## Feature 1: Continuity Monitor

### POST /api/monitor/subject

Evaluate a person across all active domains simultaneously.

**Request:**
```json
{
  "subject_id": "patient-001",
  "label": "Jane Smith",
  "domains": {
    "pharmacological": { "supply_days_remaining": 0, "..." },
    "finance": { "bank_locked": true, "..." },
    "housing": { "eviction_imminent": false, "..." }
  }
}
```

**Response includes:** `combined_state`, `domain_states`, `non_admissible_domains`, `cascading_risk`, `compound_non_admissible`, `alert`.

### POST /api/monitor/population

Evaluate a list of subjects simultaneously.

**Request:**
```json
{
  "subjects": [
    { "subject_id": "P001", "label": "Patient 1", "domains": {...} },
    { "subject_id": "P002", "label": "Patient 2", "domains": {...} }
  ]
}
```

---

## Feature 2: PNR Clocks

### POST /api/clock/register

Register a PNR clock for a case.

**Request:**
```json
{
  "case_id": "uuid",
  "label": "Benzo continuity",
  "domain": "pharmacological",
  "seconds_to_irreversibility": 7200,
  "detection_window_seconds": 600,
  "response_window_seconds": 1800,
  "recovery_window_seconds": 3600
}
```

### POST /api/clock/update

Update seconds remaining: `{ "case_id": "uuid", "seconds_remaining": 5400 }`

### GET /api/clock/all

All clocks with display, threshold, and timing margins.

### GET /api/clock/critical

Only clocks at `critical` or `CROSSED` threshold.

---

## Feature 4: Plain Language

### GET /api/plain/domains

Returns list of situation types with plain-language labels.

### GET /api/plain/questions/{domain}

Returns the question tree for the domain — each question with text, type (yes/no or numeric), and field mapping.

### POST /api/plain/evaluate

Evaluate from plain-language answers.

**Request:**
```json
{
  "domain": "pharmacological",
  "label": "Patient self-report",
  "answers": {
    "q_supply": false,
    "q_prescriber": false,
    "q_stop_risk": true,
    "q_pharmacy": false,
    "q_human": false,
    "q_fallback": false,
    "q_time": 4
  }
}
```

**Response includes:** `evaluation` (full result), `plain_explanation` (headline, explanation, recommended action, failed conditions in plain language), `translated_state` (the derived state dict).

---

## Feature 5: Research Corpus

### GET /api/corpus/patterns

Run pattern detection on the incident library. Returns most common failure conditions, escalation gap rate, domain clustering, and detected patterns.

### POST /api/corpus/export

Export anonymised corpus: `{ "anonymise": true, "domain": "optional" }`

### POST /api/corpus/regulatory

Generate regulatory submission pack: `{ "domain": "optional" }`

---

## Feature 6: Population / Cohort

### POST /api/cohort/evaluate

Evaluate a named cohort.

**Request:**
```json
{
  "cohort_id": "ward-7b",
  "label": "Ward 7B",
  "context": "NHS Trust, April 2026",
  "subjects": [
    { "subject_id": "P001", "label": "Patient 1", "domains": {...} },
    { "subject_id": "P002", "label": "Patient 2", "domains": {...} }
  ]
}
```

**Response includes:** `population_state`, `population_alert`, counts by state, `clustered_domains`, `cascade_risk_count`, `flagged_subjects`.

---

## Observability

### GET /api/observability

Cross-domain dashboard summary — state counts, recent decisions, recent non-admissible events, unresolved residue count.

### GET /api/decisions

Decision log. Optional filters: `?domain=pharmacological&state=NON-ADMISSIBLE&limit=50`

### GET /api/residue

All unresolved residue records.

### GET /api/timeline/{case_id}

Full timeline reconstruction for a case — all decisions, overrides, and residue in chronological order. Flags first non-admissible crossing.

### GET /api/incidents

Incident library search. Optional: `?domain=&state=&text=`

### POST /api/incidents/save

Save an evaluation to the incident library: `{ "evaluation_result": {...}, "notes": "optional" }`

### GET /api/audit/export

Full audit export — all decisions, overrides, unresolved residue, and summary.

---

## Meta

### GET /api/domains

List of supported domains.

### GET /api/templates

Pre-set case templates — seven scenarios across pharmacological, healthcare, finance, identity, housing, and disaster domains.

### GET /api/health

Health check. Returns status, version, active gates, active clocks.
