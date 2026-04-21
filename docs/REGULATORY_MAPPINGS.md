# Boundary — Regulatory Mappings

This document maps Boundary protocol outputs and records to relevant regulatory, governance, and safety frameworks. It is intended for use in regulatory submissions, institutional governance reviews, and compliance assessments.

---

## What Boundary produces

Boundary produces four output states and structured audit records. It does not make clinical, legal, financial, or operational decisions. It evaluates recoverability, produces admissibility states, and requires visibility and escalation.

The outputs relevant to regulatory frameworks are:

- The four boundary states (`CONTINUE`, `DEGRADED`, `NON-ADMISSIBLE`, `NON-EXECUTABLE`)
- The six recoverability conditions (RC-001 to RC-006)
- Full rule traces for every evaluation
- Residue records for every non-admissible result
- Formal override accountability records with integrity hashes
- Timeline reconstruction per case
- Population-level clustering and cascade signals
- Research corpus exports and regulatory submission packs

---

## Patient Safety

### UK — NHS Patient Safety Framework

| Boundary output | Relevance |
|---|---|
| `NON-ADMISSIBLE` / `NON-EXECUTABLE` | Corresponds to a detectable patient safety risk that requires escalation before continuation |
| Residue records | Persistent record of unresolved patient safety conditions, equivalent to open safety concerns in incident management |
| Override accountability records | Documents every instance of continuation despite flagged safety conditions — directly relevant to duty of candour and learning from incidents |
| Timeline reconstruction | Enables retrospective review of when a safety threshold was crossed and what actions were taken |
| Population view — domain clustering | Identifies systemic causes when multiple patients in the same environment fail the same domain condition simultaneously |

### RC condition mapping to patient safety criteria

| RC condition | Patient safety parallel |
|---|---|
| RC-001: Recovery path exists | A care pathway or intervention option must exist |
| RC-002: Recovery path reachable | The pathway must be accessible under real conditions (transport, staffing, availability) |
| RC-003: Failure detectable in time | Deterioration must be detectable before the irreversibility window closes |
| RC-004: Response possible in time | Clinical response capacity must be available within the required timeframe |
| RC-005: Recovery executable in time | The full intervention must be completable before irreversible harm occurs |
| RC-006: No irreversible transition before recovery | No irreversible clinical event must occur before the recovery cycle completes |

---

## Medical Device Safety

### UK — MHRA / MDR 2017/745

Boundary evaluates recoverability and produces visibility signals. It does not make clinical decisions, does not control medical devices or treatments, and does not output clinical recommendations.

The platform is a detection and escalation system. Its outputs (`CONTINUE`, `DEGRADED`, `NON-ADMISSIBLE`, `NON-EXECUTABLE`) are status signals analogous to a monitoring alert, not clinical instructions.

For any deployment in a clinical setting, the organisation deploying Boundary is responsible for determining whether the specific use case requires MHRA notification or MDR classification. The platform as shipped does not include live clinical data connections and does not execute real-world actions.

---

## Operational Risk

### Basel III / Operational Risk

| Boundary output | Operational risk parallel |
|---|---|
| `NON-ADMISSIBLE` | Operational risk threshold exceeded — process must not continue without corrective action |
| `DEGRADED` | Heightened risk state — control environment weakened |
| Override accountability records | Documented risk acceptance records with mandatory attribution |
| Residue log | Open risk items requiring resolution |
| Research corpus — escalation gap rate | Metric for time-to-detection of operational risk failures |

---

## Governance Controls

### UK Corporate Governance / FCA / CQC

| Boundary record type | Governance parallel |
|---|---|
| Override accountability record (mandatory attribution) | Board-level accountability for continuation under known risk |
| Integrity hash on override records | Tamper-evidence equivalent to signed decision records |
| Non-response residue | Documents cases where escalation was triggered but not acted on — organisational failure record |
| Timeline reconstruction | Audit trail enabling governance review of decision chronology |

---

## Infrastructure Resilience

### UK National Resilience / NCSC / CNI

| Boundary condition | Resilience parallel |
|---|---|
| RC-002: Recovery path reachable | Failover path verification |
| GI-004: Fallback path available | Backup system availability |
| `DEGRADED` state | Degraded mode operation — reduced but functional |
| Population view — cascade signals | Dependency chain failure propagation |
| Offline operation | Air-gapped or disconnected deployment capability |

---

## Social Care

### UK Care Act 2014 / CQC Fundamental Standards

| Boundary condition | Care quality parallel |
|---|---|
| `caregiver_available` (healthcare domain) | Duty of care — adequate staffing for safe continuation |
| `transport_available` | Access to care — physical accessibility of services |
| Compound non-admissibility (multi-domain) | Identifies when a person's combined circumstances constitute a safeguarding risk even when no single condition triggers an alert |
| Population view (care home cohort) | Enables oversight body review of multiple residents simultaneously |

---

## Emergency Management

### UK Civil Contingencies Act / Cabinet Office Emergency Response

| Boundary output | Emergency management parallel |
|---|---|
| `NON-EXECUTABLE` | Category 1 responder trigger — immediate action required |
| PNR clock at `critical` threshold | Time-critical resource allocation signal |
| Population view — cohort alert | Mass casualty or mass displacement assessment |
| Disaster domain rules | Evacuation window, shelter assignment, communications collapse |
| Offline mode | Operational continuity without infrastructure dependency |

---

## Research and Evidence

### Ethical use of the corpus

The research corpus module applies anonymisation before any export. Identifying fields are pseudonymised using SHA-256 hashing with a configurable salt. The anonymised corpus is suitable for:

- Epidemiological research into continuity failure patterns
- Policy analysis and institutional review
- Academic publication with appropriate ethics approval from the deploying institution
- Cross-institutional benchmarking (without identifying individual subjects or operators)

The corpus does not constitute a clinical trial, a patient registry, or a regulated research database. The deploying institution is responsible for any research ethics requirements applicable to their specific use.

---

## How to use this document in a submission

When submitting to a regulator, governance body, or institutional review:

1. Use `POST /api/corpus/regulatory` to generate a structured regulatory pack from the incident library.
2. Include the relevant section of this document as context for the Boundary protocol outputs.
3. Include the full accountability report from `POST /api/override/report` as the documented record of overrides.
4. Include timeline reconstructions for any specific cases under review.
5. Reference the Boundary Protocol Specification (`docs/BOUNDARY_SPEC.md`) as the authoritative definition of the output states.

Boundary outputs should be presented as detection and escalation signals, not as clinical or operational decisions. The decisions were made by the human operators. Boundary records when those decisions were made under non-admissible conditions.
