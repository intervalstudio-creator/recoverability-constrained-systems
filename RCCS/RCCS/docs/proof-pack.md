# Proof Pack

## Case 1 — Recoverability Failure in Home Care: Parkinson’s Misdiagnosis Risk Detected and Escalated Without Follow-Up

### Source
- Operational case DOI: https://doi.org/10.5281/zenodo.19600830

### Case summary
A bedbound patient diagnosed with Parkinson’s disease in 2022 had no structured medical follow-up until 2026.

Care was provided in a home setting by a non-clinical caregiver.

Observed conditions included:

- repeated falls
- increasing confusion
- absence of expected tremor patterns
- excessive daytime sleepiness
- loss of appetite
- lightheadedness

Symptom escalation occurred over approximately two weeks prior to intervention.

### System state
The active system included:

- patient biological state
- caregiver as operator
- healthcare system as response pathway

The system operated with:

- incomplete medical records
- no verifiable diagnosis source
- no defined follow-up pathway
- no guaranteed escalation mechanism

### Boundary evaluation
The caregiver applied the recoverability condition:

- Can the system verify patient state?
- Can the system act in time?
- Can the system ensure recovery if wrong?

At least one required condition returned:

- UNKNOWN

### Failure classification
The system was non-admissible because:

- state was not verifiable
- response was not guaranteed in time
- recovery was not assured
- escalation pathway was undefined

### Decision
Rule applied:

- UNKNOWN -> NON-ADMISSIBLE
- STOP -> ESCALATE

### Action taken
The caregiver:

- contacted the General Practitioner
- reported absence of follow-up
- reported inability to verify system state

### Response
The GP:

- could not locate records of the original diagnosis
- confirmed absence of traceable diagnostic validation

Action taken:

- patient referred for new diagnostic imaging
- neurology reassessment initiated

### Outcome
The system transitioned from:

- unverified, non-admissible state

to:

- active clinical reassessment

This restored:

- observability
- escalation pathway
- corrective action

### Counterfactual
Without application of the recoverability rule:

- symptoms may have been normalized or ignored
- no escalation would occur
- misdiagnosis or deterioration could persist

Result:

- prolonged non-admissible state
- increased probability of irreversible harm

### Validated operational conclusion
This case demonstrates that:

- absence of follow-up is structural system failure
- uncertainty in state is sufficient to trigger escalation
- non-specialists can detect boundary violations using the recoverability rule
- the recoverability condition converts uncertainty into actionable intervention
