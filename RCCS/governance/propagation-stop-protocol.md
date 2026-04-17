# Propagation Stop Protocol

If boundary evaluation returns NON_ADMISSIBLE_DO_NOT_PROPAGATE:

- do not publish
- do not relay
- do not amplify
- do not scale
- move message state away from propagation

If already propagating:
- interrupt propagation
- mark state visibly
- initiate correction or containment
