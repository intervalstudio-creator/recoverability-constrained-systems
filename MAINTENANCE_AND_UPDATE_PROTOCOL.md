# MAINTENANCE AND UPDATE PROTOCOL

This package must not drift silently.

## 1. When to update
Update when any of the following change:

- governing conditions
- runtime logic
- dependency structure
- installer behavior
- authoritative record location
- deployment assumptions
- offline/degraded execution behavior

## 2. What must be checked after every update
- Master Index still governs all derived forms
- Minimal Execution Pack remains equivalent in outcome
- RCCS implementation still preserves invariant
- preserved source bundles remain accessible
- authority map remains correct
- deployment checklist still matches real execution

## 3. Version discipline
If operational meaning changes:

- create a new version

If only formatting or minor non-semantic fixes change:

- minor correction is acceptable

## 4. Drift rule
If any representation, implementation, summary, or bundle component diverges in admissibility outcome from the authoritative governing form:

- equivalence is broken
- affected component is non-admissible until corrected

## 5. Sustainment rule
At regular intervals verify:

- files remain accessible
- runtime still executes
- dependencies remain available
- offline forms remain usable
- authoritative links and DOI references still resolve

If sustainment cannot be established in time under real conditions:

- continuation is non-admissible where affected
