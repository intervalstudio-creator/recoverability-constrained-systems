# Execution Model

RCCS operates through a recoverability-constrained propagation loop:

IDENTITY -> MESSAGE -> VALIDATION -> PROPAGATION -> CHALLENGE -> RESOLUTION -> STATE

Propagation is admissible only while the loop remains recoverable in time under real conditions.

## Required inputs

Every propagation decision must evaluate:

- state visibility
- time-to-irreversibility
- response capacity
- recovery capacity

## Admissibility outputs

- ADMISSIBLE_TO_PROPAGATE
- NON_ADMISSIBLE_DO_NOT_PROPAGATE

## Binding rule

If any required condition becomes invalid during propagation:

- propagation must be interrupted
- state must transition away from propagation
