# Recoverability-Constrained Communication System (RCCS)

RCCS is the communication-domain execution form of the Recoverability-Constrained Systems framework.

It does not independently redefine admissibility.
It implements the recoverability boundary condition for message propagation under online, offline, paper, device, and human relay conditions.

## Canonical publications

- RCCS canonical publication: https://doi.org/10.5281/zenodo.19596392
- Operational one-page (executable form): https://doi.org/10.5281/zenodo.19600684
- Parkinson's misdiagnosis risk case: https://doi.org/10.5281/zenodo.19600830
- Systemic failure cases: https://doi.org/10.5281/zenodo.19600917

## Invariant

A message may propagate only while its validity remains recoverable in time under real conditions.

If it cannot be:

- verified
- challenged
- corrected

then:

- propagation is non-admissible
- execution does not occur

## Execution-complete form

This repository defines the complete, execution-ready form of RCCS.

It integrates:

- human communication layer
- paper continuity layer
- offline device runtime
- structured challenge and correction
- propagation stop conditions
- communication-domain boundary evaluation

This does not modify the invariant or core system logic.
It completes execution under real-world constraints.}
Includes validated real-world proof cases in `docs/proof-pack.md`.

## Communication-domain boundary evaluation

RCCS evaluates four required inputs before propagation:

- state visibility
- time-to-irreversibility
- response capacity
- recovery capacity

If any required input cannot be established in time under real conditions:

- message propagation is non-admissible
- propagation must not occur

## Minimal operational rule

A message may propagate only while its validity remains recoverable across origin, present state, and future correction in time under real conditions.

If this cannot be established:

- it does not propagate

## Closure

No partial interpretation is valid.
All forms in this repository must preserve the same admissibility outcome.
If online, offline, paper, human, or device forms diverge in outcome, the system is non-admissible until equivalence is restored.


## Original Artifact Preservation

This repository also preserves the prior RCCS full artifact bundle under:

- `original_artifacts/`

These files are retained without loss and include:

- API specification
- architecture record
- database schema
- explanation preview
- governance and protocol PDF
- institutional message
- MVP implementation specification
- integrated master document
- master overview
- system specification
- UI/UX specification
- website block
- original README

The structured repo and the preserved artifacts must be interpreted together as non-fragmentable components of the same RCCS execution system.
