# Recoverability-Constrained Communication System (RCCS)

## Invariant
A message may propagate only while its validity remains recoverable in time under real conditions.
If it cannot be verified, challenged, or corrected:
-> propagation is non-admissible

## Canonical execution loop
IDENTITY -> MESSAGE -> VALIDATION -> PROPAGATION -> CHALLENGE -> RESOLUTION -> STATE

## Core layers
1. Identity layer
- persistent identity
- unique account
- verified human or verified organization
- no single-point identity dependence for continuity-critical use

2. Message layer
Each message is a structured object:
- claim
- context
- optional reference
- timestamp
- author identity
- state
- carrier
- acknowledgment status

3. Admissibility gate
A message may scale only if:
- it can be evaluated
- it can be challenged
- it can be corrected
- correction can reach the exposure field
Otherwise it remains local or is blocked.

4. Propagation control
No virality by default.
Propagation levels:
- Local
- Limited
- Expanded
- Wide
Movement upward depends on message stability and challenge state.

5. Challenge layer
Challenges are structured:
- factual contradiction
- logical inconsistency
- missing evidence
- misleading framing

6. Resolution layer
States:
- unverified
- contested
- under_resolution
- stable
- corrected
- invalid

7. Recovery layer
Corrections must reach the same audience exposed to the original message.
If correction cannot reach the exposure field, original propagation was non-admissible.

## Execution-complete layer
RCCS operates in three equivalent forms:
- Human execution form: voice, gesture, paper relay, physical signal, direct acknowledgment
- Paper continuity form: structured sheets, state labels, correction logs, identity recovery
- Offline device runtime form: peer-to-peer transfer, store-and-forward routing, delayed sync

Messages must remain challengeable and correctable across all three forms.
If communication stops while an alternative carrier exists, the system is degraded.

## Product rule
Engagement does not determine reach.
Validity state determines reach.

## Anti-bot rule
Identity must be costly to fake and cheap to maintain.

## Terminal rule
A communication system is admissible only while truth remains recoverable in time under real conditions.
