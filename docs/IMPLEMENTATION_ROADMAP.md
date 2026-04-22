# Implementation Roadmap

This roadmap uses the reviewed reference pack plus the current repo state.

It is ordered to preserve the invariant first, then expand scope safely.

## Guiding rule

Every step below must preserve:
- invariant fidelity
- state correctness
- timestamped formal record generation
- downloadable output
- static-hostable deployment

## Phase 1: Stabilize the current website surface

Goal:
Make the existing `web/` implementation reliable, coherent, and maintainable before adding more domains.

Tasks:
- verify all active tabs and flows in `web/` against real browser behavior
- normalize state naming across UI, record, and export layers
- remove leftover branding drift where `Boundary` appears instead of `RECOVS`
- verify profile, trusted, group, witness, on-behalf, and check-in flows
- add lightweight regression checks for core evaluation and export behavior

Definition of done:
- the static website runs cleanly
- record generation works across all current tabs
- no broken tab or export flows remain

## Phase 2: Expand exports, not logic

Goal:
Make the current evaluation outputs more reusable by institutions without changing admissibility logic.

Tasks:
- add plain-text record export
- add markdown record export
- add authority summary export
- add institution handoff summary export
- add a bundled escalation package export from a finished evaluation

Definition of done:
- one completed case can produce multiple authority-ready outputs quickly

## Phase 3: Add communication-event evaluation

Goal:
Implement the first major missing domain from the reference pack.

Tasks:
- create an `Evaluate Post` workflow
- capture claim, platform, link, screenshot reference, and correction status
- evaluate whether correction is still possible in time
- determine whether propagation is recoverable
- generate a formal communication-event record using the same admissibility grammar

Definition of done:
- the communication-event path produces the same class of formal output as incident evaluation

## Phase 4: Add chain-of-events timeline support

Goal:
Move from single-event records to linked event chains.

Tasks:
- add timeline event entry
- support original event, amplification, contradiction, platform action, authority response, and collapse point
- generate one combined formal chain record
- preserve event timestamps and sequence trace

Definition of done:
- a user can turn multiple related events into one escalation-ready timeline

## Phase 5: Add platform-action review

Goal:
Evaluate whether a platform’s own intervention is itself recoverable and attributable.

Tasks:
- add workflow for account restriction / content removal / failed appeal
- capture missing explanation, lack of remedy, and timing impact
- determine whether re-entry or correction remains possible
- generate a formal platform-action record

Definition of done:
- platform restrictions can be evaluated using the same recoverability logic as other domains

## Phase 6: Build a dedicated escalation package surface

Goal:
Turn RECOVS from a strong record generator into a full escalation package builder.

Tasks:
- bundle evaluation summary, formal record, failure trace, recommended authority path, and communication-ready text
- support authority-specific packaging when possible
- preserve DOI references and evaluation traceability

Definition of done:
- a completed case can be exported as a ready-to-send package with minimal editing

## Phase 7: Internal cleanup and modularization

Goal:
Reduce website complexity without breaking the static build.

Tasks:
- split `web/app.js` into logical modules if static hosting remains unchanged
- separate evaluation logic from UI concerns
- separate export builders from input flows
- document module boundaries in `docs/`

Definition of done:
- the website remains static-hostable but easier to maintain and extend

## Immediate top 10 implementation gaps

1. Full browser verification of all current tabs and exports
2. Branding normalization from older `Boundary` remnants to `RECOVS`
3. Communication-event workflow
4. Chain-of-events builder
5. Platform-action review workflow
6. Escalation package export surface
7. Plain-text / markdown / authority summary exports
8. Lightweight regression tests for state and export behavior
9. Clear modular structure for the growing `web/app.js`
10. Better contributor-facing doc links from the repo root

## Practical next task recommendation

If only one major new feature is added next, it should be:

`Evaluate Post`

Reason:
- it is clearly required by the reference pack
- it extends RECOVS into communication-event admissibility without disturbing existing incident flows
- it creates a clean path toward chain-of-events and platform-action review
