# DEPLOYMENT CHECKLIST

Use this before any domain deployment.

## Core admissibility
- [ ] Boundary defined
- [ ] Time to irreversibility established
- [ ] Detection path exists
- [ ] Response path exists
- [ ] Recovery path exists
- [ ] All required dependencies identified
- [ ] All required resources present and reachable in time
- [ ] Authority to act exists and is executable in time

## Execution
- [ ] STOP condition is binding
- [ ] Mid-execution re-evaluation exists
- [ ] Material state change invalidates prior admissibility
- [ ] Interface/handoff checks exist
- [ ] Offline/degraded mode has been validated
- [ ] No black-box dependency blocks verification

## Testing
- [ ] Delay tested
- [ ] Hidden state tested
- [ ] Failure tested
- [ ] Uncertainty tested
- [ ] Drift tested
- [ ] Overload tested
- [ ] Dependency loss tested
- [ ] External shock tested

## Proof
- [ ] At least one real case mapped
- [ ] Boundary point identified
- [ ] Escalation point identified
- [ ] Expected interruption/containment path defined

## Final rule
If any required item is incomplete, assumed, or unverified:

- deployment is non-admissible
- execution must not occur
