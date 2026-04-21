# Boundary Protocol Specification v1.1

**Open Standard — Recoverability-Constrained Execution**

---

## 1. Purpose

The Boundary Protocol defines a standard runtime grammar for evaluating recoverability-constrained systems. It specifies:

- The four output states and their formal definitions
- The six recoverability conditions that constitute the execution constraint
- The evaluation grammar — rules, weights, layers
- The audit residue format
- The override accountability requirements
- The escalation chain structure
- The continuity object model for cross-domain evaluation
- The population-level evaluation model

This specification is independent of implementation language and deployment environment. A conforming implementation may be written in any language, deployed on any platform, and used in any domain.

---

## 2. Output States

The Boundary Protocol defines exactly four output states. No other outputs are valid.

### 2.1 CONTINUE

All recoverability conditions evaluated in the applicable rule packs are satisfied. Execution is admissible under current state. No immediate action required. Continue with monitoring.

### 2.2 DEGRADED

One or more conditions of `major` weight have failed. The system remains technically admissible but margin is reduced. Monitoring frequency must increase. Fallback path must be identified and verified. Act before the state worsens.

### 2.3 NON-ADMISSIBLE

One or more conditions of `critical` weight have failed, or one or more fields required by a critical rule are unknown. Execution is not admissible. The process must stop, stabilise, or transition to a valid fallback state. A responsible human authority must be notified.

### 2.4 NON-EXECUTABLE

`NON-ADMISSIBLE` conditions are present and one or more of the following also hold:

- Human authority is not reachable within the timing window
- Time remaining before irreversibility is less than one hour
- Time remaining is zero or negative

When `NON-EXECUTABLE`, escalation is required and continuation must not occur. The system cannot resolve this state autonomously. A responsible human authority must be reached immediately.

---

## 3. The Six Recoverability Conditions

These are the foundational conditions of the execution constraint. All six must hold for execution to be admissible. They are evaluated before any domain-specific rules, in every case, in every domain.

| Rule ID | Field | Condition |
|---|---|---|
| RC-001 | `recovery_path_exists` | A recovery path must exist |
| RC-002 | `recovery_path_reachable` | The recovery path must be reachable under real conditions |
| RC-003 | `failure_detectable_in_time` | Failure must be detectable before the irreversibility threshold |
| RC-004 | `response_possible_in_time` | A response must be possible within the available time window |
| RC-005 | `recovery_executable_in_time` | Recovery must be fully executable before irreversible transition |
| RC-006 | `no_irreversible_transition_before_recovery` | No irreversible transition must occur before recovery completes |

Failure of any single condition → `NON-ADMISSIBLE`.

---

## 4. Rule Grammar

### 4.1 Rule structure

```json
{
  "id": "DOMAIN-NNN",
  "field": "state_field_name",
  "required_value": true,
  "required_min": null,
  "required_max": null,
  "conditional_on": "other_field",
  "weight": "critical | major | minor | execution_gate",
  "description": "Human-readable condition statement"
}
```

### 4.2 Weight semantics

| Weight | Failure effect |
|---|---|
| `critical` | → `NON-ADMISSIBLE` or `NON-EXECUTABLE` |
| `execution_gate` | → `NON-EXECUTABLE` when combined with any critical failure |
| `major` | → `DEGRADED` (unless critical also fails) |
| `minor` | Logged in trace only — no state change |

### 4.3 Unknown fields

A field not present in the input state is unknown. Unknown on a critical rule = unestablished recoverability = `NON-ADMISSIBLE`. This is not `DEGRADED`. Unestablished recoverability is not a weakened state — it is a missing state. A missing state cannot establish admissibility.

### 4.4 Conditional rules

A rule with `conditional_on` is only evaluated if the named field is `true` in the state. If the condition is not active, the rule is skipped. Skipped rules do not contribute to pass or fail counts.

---

## 5. Layered Evaluation

Evaluation proceeds in three layers, in order:

**Layer 1 — Six Recoverability Conditions (RC-001 to RC-006)**

Always evaluated first. Critical weight. Failure of any → `NON-ADMISSIBLE`.

**Layer 2 — Execution Gate Conditions**

- `GI-001`: Human authority reachable (`execution_gate` weight)
- `GI-002`: Time remaining positive (`execution_gate` weight)
- `GI-003`: Override attributed (critical, conditional on override_active)
- `GI-004`: Fallback path available (major weight)

Execution gate failure combined with any critical failure → `NON-EXECUTABLE`.

**Layer 3 — Domain-Specific Rules**

Domain rule packs define the conditions specific to each recoverability domain. See Section 6.

---

## 6. Domain Rule Packs

Each domain defines a rule pack of `critical`, `major`, and `minor` conditions. Domain rules extend the six recoverability conditions with domain-specific evaluations. The currently defined domains are:

`pharmacological`, `healthcare`, `identity`, `finance`, `housing`, `legal`, `labour`, `education`, `infrastructure`, `disaster`, `transport`, `energy`, `communications`, `food_water`, `supply_chain`

New domain rule packs may be defined without modifying the core protocol. A conforming implementation must evaluate all six RC conditions regardless of which domain rule pack is applied.

---

## 7. Evaluation Input Schema

```json
{
  "domain": "string — one of the supported domains",
  "label": "string — human description of the case",
  "case_id": "string — optional, auto-generated if absent",
  "operator_id": "string — identity of the evaluating operator",
  "state": {
    "recovery_path_exists": "boolean",
    "recovery_path_reachable": "boolean",
    "failure_detectable_in_time": "boolean",
    "response_possible_in_time": "boolean",
    "recovery_executable_in_time": "boolean",
    "no_irreversible_transition_before_recovery": "boolean",
    "human_authority_reachable": "boolean",
    "time_remaining_seconds": "integer",
    "fallback_path_available": "boolean",
    "override_active": "boolean",
    "override_attributed": "boolean",
    "...domain-specific fields...": "values"
  }
}
```

---

## 8. Evaluation Output Schema

```json
{
  "eval_id": "uuid",
  "case_id": "uuid",
  "label": "string",
  "domain": "string",
  "operator_id": "string",
  "timestamp": "ISO 8601",
  "boundary_state": "CONTINUE | DEGRADED | NON-ADMISSIBLE | NON-EXECUTABLE",
  "failed_conditions": [
    {
      "rule_id": "string",
      "name": "string",
      "description": "string",
      "layer": "global_invariant | domain",
      "weight": "critical | execution_gate | major | minor",
      "passed": false,
      "reason": "string"
    }
  ],
  "unknown_fields": [...],
  "time_to_irreversibility": {
    "seconds_remaining": "integer",
    "hours_remaining": "float",
    "point_of_no_return_crossed": "boolean",
    "margin_warning": "boolean"
  },
  "rule_trace": [...],
  "passed_count": "integer",
  "failed_count": "integer",
  "unknown_count": "integer",
  "total_rules_evaluated": "integer"
}
```

---

## 9. Audit Residue

Every `NON-ADMISSIBLE` or `NON-EXECUTABLE` result must produce a residue record. Residue persists until explicitly resolved by a named authority. Unresolved residue must appear in all observability outputs. Nothing important is silent.

### Residue schema

```json
{
  "residue_id": "uuid",
  "case_id": "uuid",
  "residue_type": "string",
  "description": "string",
  "logged_at": "ISO 8601",
  "resolved": "boolean",
  "resolved_by": "string",
  "resolved_at": "ISO 8601",
  "resolution_note": "string"
}
```

---

## 10. Override Accountability

An override is any act of continuation following a `NON-ADMISSIBLE` or `NON-EXECUTABLE` result. The following fields are mandatory for every override record:

| Field | Type | Description |
|---|---|---|
| `operator_id` | string | Identity of the operator continuing |
| `operator_role` | string | Role of the operator |
| `authorising_authority` | string | Name and role of the person authorising continuation |
| `reason` | string | Stated reason for continuation |
| `acknowledged_risk` | string | The risk being accepted and any mitigations |
| `timestamp` | ISO 8601 | When the override occurred |
| `original_boundary_state` | string | The state at the time of override |
| `integrity_hash` | SHA-256 | Tamper-evidence hash of the full record |

An override record without full attribution is itself a boundary violation and must produce its own residue record. Override records must be tamper-evident.

---

## 11. Escalation Chain

When `NON-EXECUTABLE`:

1. The system logs the escalation with case ID, domain, timestamp, and reason.
2. An escalation residue record is created and remains unresolved until a named authority explicitly acknowledges it.
3. The system must not autonomously resolve a `NON-EXECUTABLE` state.
4. If the human authority does not respond within the timing window, this must be logged as a non-response residue.
5. Non-response residue is itself a boundary failure and must propagate to the cross-domain dashboard.

---

## 12. Continuity Object Model

A continuity object represents a person or process evaluated across multiple domains simultaneously.

```json
{
  "subject_id": "string",
  "label": "string",
  "domains": {
    "domain_name": { "...domain state..." }
  }
}
```

A continuity object evaluation produces:

- Per-domain boundary states
- Combined state (worst across all domains)
- Non-admissible domain list
- Cascading risk map (failing domains → at-risk dependent domains)
- Compound non-admissibility flag (multiple degraded domains = combined non-admissible)

The combined state is the worst individual domain state. Compound non-admissibility is raised when three or more domains are simultaneously `DEGRADED` even if none individually triggers `NON-ADMISSIBLE`.

---

## 13. Point-of-No-Return Clock

A PNR clock tracks the time-to-irreversibility for a case and degrades through defined thresholds:

| Threshold | Seconds remaining | Required action |
|---|---|---|
| `safe` | > 604,800 (7 days) | Continue monitoring |
| `monitor` | ≤ 604,800 | Increase monitoring frequency |
| `degraded` | ≤ 86,400 (24 hours) | Active intervention required |
| `warning` | ≤ 14,400 (4 hours) | Urgent action required |
| `critical` | ≤ 3,600 (1 hour) | Escalate immediately |
| `CROSSED` | ≤ 0 | Point of no return has passed |

The PNR clock also tracks the timing margins for detection, response, and recovery windows separately. If the sum of these three margins exceeds the time remaining, the situation is non-executable regardless of other conditions.

---

## 14. Population Evaluation

A population evaluation applies continuity object evaluation to a cohort simultaneously.

Systemic signals:
- Three or more subjects failing the same domain = domain clustering = possible systemic cause
- 30% or more of subjects in `DEGRADED` state = population degradation threshold
- Any subject in `NON-EXECUTABLE` state = immediate escalation

Trend detection compares consecutive population snapshots and classifies the trajectory as `WORSENING`, `IMPROVING`, or `STABLE`.

---

## 15. Offline Operation

A conforming implementation must be capable of evaluating cases without:
- Internet connectivity
- Cloud authentication
- External APIs

Offline evaluations must be logged locally and synchronised when connectivity is restored. The offline state must be clearly indicated to the operator. Offline evaluations are as valid as online evaluations — the same rules, weights, and states apply.

---

## 16. Research Corpus

An implementation that retains evaluation records accumulates a structured corpus of recoverability failures. This corpus must support:

- Anonymisation of identifying fields before research export
- Pattern detection across the corpus
- Export in open formats (JSON, CSV)
- Regulatory submission pack generation

The corpus is a research and policy asset. Access to non-anonymised records must be restricted to authorised operators.

---

## 17. What this protocol is not

The Boundary Protocol:
- Does **not** make clinical, legal, financial, or operational decisions
- Does **not** authorise or block actions autonomously
- Does **not** replace human judgment or human authority
- Does **not** produce outputs beyond the four defined states
- Does **not** operate as a medical device, legal instrument, or financial system

Every output of the Boundary Protocol must be acted on by a responsible human authority.
