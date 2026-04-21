# Boundary — Changelog

---

## v4.1 (current)

### New features

**1. Cross-Institutional Continuity Monitor** (`engine/continuity_monitor.py`)
- Evaluates a person across all active domains simultaneously as a continuity object
- Detects compound non-admissibility: three or more domains degraded simultaneously = non-admissible combined picture invisible to any single institution
- Detects cascading domain dependencies
- Population evaluation: evaluates a cohort simultaneously
- API: `POST /api/monitor/subject`, `POST /api/monitor/population`

**2. Point-of-No-Return Clock** (`engine/ponr_clock.py`)
- Live countdown per case before irreversible transition
- Four thresholds: monitor → degraded → warning → critical → CROSSED
- Timing margin breakdown: detection, response, recovery windows separately
- Registry of all active clocks with summary
- API: `POST /api/clock/register`, `POST /api/clock/update`, `GET /api/clock/all`, `GET /api/clock/critical`

**3. Override Accountability Record** (`engine/override_accountability.py`)
- Formal, tamper-evident record for every override
- SHA-256 integrity hash — detects any post-creation modification
- All attribution fields mandatory: operator, role, authorising authority, reason, acknowledged risk
- Accountability report with integrity verification
- API: `POST /api/override/formal`, `POST /api/override/report`, `GET /api/override/records`

**4. Plain-Language Case Builder** (`engine/plain_language.py`)
- Step-by-step question flow in ordinary words for six domains
- Translates answers to formal recoverability evaluation
- Returns results in plain language with headline, explanation, recommended action
- Same engine, same states, same rule trace as expert evaluation
- API: `GET /api/plain/domains`, `GET /api/plain/questions/{domain}`, `POST /api/plain/evaluate`

**5. Research Corpus** (`engine/research_corpus.py`)
- Pattern detection across accumulated evaluation records
- Anonymisation pipeline (SHA-256 pseudonymisation)
- Export: JSON, CSV, regulatory submission packs
- Metrics: escalation gap rate, domain clustering, avg timing at non-admissible
- API: `GET /api/corpus/patterns`, `POST /api/corpus/export`, `POST /api/corpus/regulatory`

**6. Population-Level Continuity View** (`engine/population_view.py`)
- Named cohort evaluation
- Domain clustering detection (3+ subjects failing same domain = systemic signal)
- Population degradation threshold (30%+ degraded)
- Snapshot comparison: WORSENING / IMPROVING / STABLE
- API: `POST /api/cohort/evaluate`

### Documentation

- README rewritten for v4.1
- `docs/BOUNDARY_SPEC.md` updated to v1.1 — adds RC conditions, continuity object model, PNR clock thresholds, population evaluation model
- `docs/FEATURES.md` — new: full description of all six feature modules
- `docs/API_REFERENCE.md` — new: complete endpoint reference
- `docs/DEPLOYMENT.md` — new: local, institutional, offline, and field deployment
- `docs/REGULATORY_MAPPINGS.md` — new: mapping to patient safety, medical device, operational risk, governance, resilience, and emergency management frameworks

### UI additions

Expert mode — six new sidebar panels:
- Person Monitor
- Population View
- PNR Clocks
- Accountability Records
- Plain Language Evaluator
- Research Corpus

### API additions

Twelve new endpoints across six feature areas. Health endpoint updated to v4.1.0 and now includes active clock count.

---

## v4.0

- Core engine rebuilt with six-condition recoverability model (RC-001 to RC-006)
- Output states corrected to `CONTINUE / DEGRADED / NON-ADMISSIBLE / NON-EXECUTABLE`
- Unknown field handling corrected: unknown on critical rule = NON-ADMISSIBLE (not DEGRADED)
- Layered evaluation: RC conditions → execution gates → domain rules
- 15 domain rule packs
- Continuous re-gating
- Cross-domain propagation
- Full observability and audit module
- FastAPI server with 19 endpoints
- Expert + simple + offline UI modes
- GitHub Actions CI
- Test suite

---

## v3.2 (prior)

- Core decision engine
- Bounded execution layer
- Observability and audit logging
- External actuation connectors
- Event-driven evaluation
- Continuity workflows for identity, finance, transport, disaster
- Local UI
- Pharmacological Systems Layer (benzodiazepine protocol)
