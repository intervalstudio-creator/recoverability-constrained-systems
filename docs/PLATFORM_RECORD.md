# Boundary Platform v4.1 â€” Recoverability-Constrained Execution System (Technical Record and Executable Release)

**Framework:** Recoverability-Constrained Systems
**Type:** Platform Technical Record â€” Executable Release
**Version:** 4.1
**Repository:** https://github.com/intervalstudio-creator/recoverability-constrained-systems
**Status:** Executable Platform â€” Technical Record

---

## Abstract

This record documents Boundary v4.1: the execution system for the Recoverability-Constrained Systems framework. Boundary is a functioning platform, not a theoretical model. It evaluates recoverability in real time, produces the four authoritative output states, and requires visibility and escalation when continuation is non-admissible.

This record provides the technical specification, architectural overview, feature documentation, and authoritative citation reference for the v4.1 release. It is intended to make the platform citable in academic, regulatory, and institutional contexts.

---

## 1. What Boundary Does

Boundary detects when continuation becomes non-recoverable in time under real conditions and requires visibility and escalation when it does.

It evaluates the six recoverability conditions for every case in every domain. It produces exactly four output states:

| State | Meaning |
|---|---|
| CONTINUE | All recoverability conditions met. Execution admissible. |
| DEGRADED | One or more conditions weakened. Margin reduced. Act. |
| NON-ADMISSIBLE | Recoverability cannot be established. Execution must not proceed. |
| NON-EXECUTABLE | Non-admissible and time-critical or authority unreachable. Escalate immediately. |

Boundary evaluates recoverability and produces admissibility states. It does not make or enforce clinical, legal, financial, or operational decisions. All outputs require action by a responsible human authority.

---

## 2. The Six Recoverability Conditions

Evaluated for every case, in every domain, before domain-specific rules:

| Rule | Condition |
|---|---|
| RC-001 | Recovery path exists |
| RC-002 | Recovery path is reachable under real conditions |
| RC-003 | Failure detectable in time |
| RC-004 | Response possible in time |
| RC-005 | Recovery executable in time |
| RC-006 | No irreversible transition before recovery |

---

## 3. Supported Domains (v4.1)

pharmacological Â· healthcare Â· identity Â· finance Â· housing Â· legal Â· labour Â· education Â· infrastructure Â· disaster Â· transport Â· energy Â· communications Â· food_water Â· supply_chain

---

## 4. Architecture

```
engine/
â”œâ”€â”€ boundary_engine.py          Core evaluation engine
â”œâ”€â”€ continuity_monitor.py       Cross-institutional continuity monitor
â”œâ”€â”€ ponr_clock.py               Point-of-no-return clock registry
â”œâ”€â”€ override_accountability.py  Formal tamper-evident override records
â”œâ”€â”€ plain_language.py           Plain-language case builder
â”œâ”€â”€ research_corpus.py          Pattern detection and regulatory export
â””â”€â”€ population_view.py          Population-level cohort evaluation

api/server.py                   FastAPI REST server (35+ endpoints)
web/index.html                  Public RECOVS UI â€” records, evaluation, and exports
observability/observability.py  Decision trace, residue, audit, incident library
```

---

## 5. New in v4.1 â€” Six Feature Modules

### 5.1 Cross-Institutional Continuity Monitor

Evaluates a person as a continuity object across all active domains simultaneously. Implements the Human Continuity Graph model. Detects compound non-admissibility (multiple degraded domains creating a combined non-admissible state invisible to single-domain evaluation) and cascading domain dependencies.

### 5.2 Point-of-No-Return Clock

Live countdown per case before irreversible transition. Four thresholds: monitor â†’ degraded â†’ warning â†’ critical â†’ CROSSED. Tracks detection, response, and recovery timing margins separately.

### 5.3 Override Accountability Record

Formal, tamper-evident record for every override. SHA-256 integrity hash. All attribution fields mandatory. Suitable for regulatory review and legal proceedings.

### 5.4 Plain-Language Case Builder

Step-by-step question flow in ordinary language for six domains. Translates answers to a formal recoverability evaluation. Returns results in plain language. Same engine, same states, same rule trace as expert evaluation.

### 5.5 Research Corpus

Pattern detection across accumulated evaluation records. Anonymisation pipeline. Export: JSON, CSV, regulatory submission packs. Metrics: escalation gap rate, domain clustering, average timing at non-admissible states.

### 5.6 Population-Level Continuity View

Evaluates a cohort simultaneously. Domain clustering (3+ subjects failing same domain = systemic signal). Population degradation threshold. Snapshot trend comparison: WORSENING / IMPROVING / STABLE.

---

## 6. API Surface

The Boundary v4.1 API provides 35+ endpoints across:
- Core evaluation (single, batch, paths, propagation, event-driven evaluation)
- Escalation and override accountability
- Continuous re-gating
- Cross-institutional monitoring (subject and population)
- PNR clock registry
- Plain-language evaluation
- Research corpus
- Cohort evaluation
- Full observability and audit

Base URL: `http://127.0.0.1:8787`
Full reference: `docs/API_REFERENCE.md`

---

## 7. Offline Operation

The full evaluation engine runs in-browser as a JavaScript mirror of the Python engine. All four states, all six RC conditions, and all domain rules are available without backend connection. Offline evaluations are stored locally for audit. Offline mode performs evaluation only and does not execute or trigger external actions.

---

## 8. Relationship to Authoritative Framework Records

This platform operationalizes:

- Recoverability-Constrained Execution â€” Universal Constraint on Autonomous, Human, and Hybrid Systems (Closed Form): https://doi.org/10.5281/zenodo.19670123
- Recoverability-Constrained Systems â€” Universal Execution Constraint and Cross-Domain Continuity Architecture (Ultimate Unified Closed Form): https://doi.org/10.5281/zenodo.19671515
- Universal Admissibility Evaluation Standard (UAES): https://doi.org/10.5281/zenodo.19644299
- Master Deployment Module (MDM-001): https://doi.org/10.5281/zenodo.19655998
- Master Index: https://doi.org/10.5281/zenodo.19583410

Pharmacological domain records:
- Substance, Material, and Interval Systems: https://doi.org/10.5281/zenodo.19664442
- Benzodiazepine Protocol: https://doi.org/10.5281/zenodo.19664722
- Pharmacological Systems Architecture: https://doi.org/10.5281/zenodo.19664810

---

## 9. How to Cite

When citing the Boundary platform in academic, regulatory, or institutional contexts, reference this record and the repository:

> Boundary Platform v4.1 â€” Recoverability-Constrained Execution System. Recoverability-Constrained Systems framework. Repository: https://github.com/intervalstudio-creator/recoverability-constrained-systems. [This Zenodo DOI].

---

## 10. Important

Boundary evaluates recoverability and produces admissibility states. It does not make or enforce clinical, legal, financial, or operational decisions. All outputs require action by a responsible human authority. This build does not include live credentials and does not execute real-world actions.

