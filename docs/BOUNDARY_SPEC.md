## Boundary Specification

Boundary is a public recoverability evaluation framework.

This public specification preserves only:

- the core principle
- the four output states
- the public-facing evaluative purpose of the system

Boundary does not publish operational implementation detail in this repository.

### Core principle

A system may evaluate, simulate, or recommend without restriction.

A system may only act where recoverability can be established in time under real conditions as sufficient to prevent irreversible transition.

If recoverability cannot be established:

- continuation is non-admissible
- execution does not occur

### Public output states

- `CONTINUE`
- `DEGRADED`
- `NON-ADMISSIBLE`
- `NON-EXECUTABLE`

### Public note

This repository is intentionally reduced for public release.
