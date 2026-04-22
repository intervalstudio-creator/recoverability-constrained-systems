# Website Direction Gap Analysis

This document compares the reviewed release snapshot in the reference zip with the current repository website at `web/`.

## Baseline

The release snapshot showed a broader, self-contained RECOVS website direction centered on:
- incident evaluation
- communication-event evaluation
- chain-of-events capture
- platform-action review
- escalation package generation

The current repo website already includes:
- incident-style recoverability evaluation
- formal record generation
- downloadable PDF / HTML / JSON outputs
- institution-facing export and packet flows
- lock card
- profile and trusted contact storage
- group mode
- witness and on-behalf records
- local check-in

## Where the current repo is already strong

Compared with the release snapshot, the current repo website is already stronger in:
- evidence-style PDF generation
- UTC evaluation IDs and tamper-evident hashes
- institution handoff packaging
- country-aware support organisations
- offline-friendly static deployment
- locally stored user profile and support flows

These are aligned with the reference pack and should be preserved.

## Biggest remaining gaps

The largest gaps between the release snapshot direction and the current repo website are not cosmetic. They are domain and workflow gaps.

### 1. Communication-event evaluation is still missing

The release snapshot clearly pointed toward evaluating:
- posts
- screenshots
- claims
- verifiability
- correction possibility
- propagation risk

The current website does not yet provide a dedicated communication-event workflow.

### 2. Chain-of-events tooling is still missing

The release snapshot treated event chains as first-class:
- original claim
- amplification
- contradiction
- platform action
- authority response
- collapse point

The current website records single evaluations well, but it does not yet model linked event chains.

### 3. Platform-action review is still missing

The release pack explicitly described review of:
- removals
- locks
- restrictions
- non-transparent enforcement
- broken appeal paths

This is not yet present in the current repo website.

### 4. Escalation package generation is only partial

The current website creates strong downloadable records and institution packets, but it does not yet expose a dedicated escalation-package workflow that bundles:
- summary
- state
- failures
- trace
- target authority handoff
- communication-ready output variants

### 5. Export variants are still narrower than the reference direction

The pack suggested preserving and expanding:
- printable record layout
- plain-text export
- markdown export
- authority summary
- institution summary

The current site has strong HTML/PDF/JSON paths, but not the full export family yet.

## Important non-gaps

The release snapshot should not be interpreted as a requirement to revert the repo website back to a darker self-contained one-file build.

That snapshot was directionally useful, but the current repo website is already better in several important ways:
- clearer institution-ready documentation output
- stronger record traceability
- stronger export path
- better growth path for modular static hosting

So the right move is feature extraction, not rollback.

## Recommended feature extraction from the snapshot

The release snapshot is most valuable as a source of future modules:

1. `Evaluate post`
   Add a communication-event workflow with fields for platform, claim, evidence, correction possibility, and propagation risk.

2. `Chain of events`
   Add a timeline-builder that links multiple events into one formal escalation sequence.

3. `Platform action`
   Add a review path for platform restrictions, removals, appeal failures, and non-transparent enforcement outcomes.

4. `Escalate`
   Add a dedicated escalation package builder that turns a completed evaluation into multiple delivery formats.

## Bottom line

The current repo website is already a stronger formal-record surface than the zip snapshot.

The next step is not to replace it. The next step is to absorb the missing domain workflows from that snapshot while preserving the stronger RECOVS evidence-generation layer already in the repo.
