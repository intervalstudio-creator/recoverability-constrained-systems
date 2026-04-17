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

---

## Case 2 — Research Platform Account Termination Without Recovery Path (Figshare)

### Source
- Operational case DOI: https://doi.org/10.5281/zenodo.19597602

### Case summary
A research account containing over 120 interdependent publications forming a unified system was disabled by the hosting platform.

The platform:

- removed access to all hosted materials
- provided no appeal mechanism
- offered only metadata and file export

### System state
The platform functioned as a critical dependency for:

- access
- verification
- citation integrity
- continuity of the research corpus

System characteristics:

- single-point dependency
- non-fragmentable document structure
- continuity dependent on persistent access

### Boundary evaluation

- Can access be restored in time? → NO  
- Can escalation resolve the state? → NO  
- Can the system recover continuity? → NO  

### Failure classification

- access and reachability failure  
- re-entry failure  
- dependency collapse  
- escalation resolution failure  
- non-bypassable control  
- recoverability condition failure  

### Decision

- RECOVERABILITY = NOT ESTABLISHABLE  
- NON-ADMISSIBLE  

→ continuation of reliance on this platform is not allowed  

### Action taken

- system reconstituted using:
  - Zenodo
  - GitHub
  - independent storage

### Outcome

- removal of single-point dependency  
- restoration of access pathways  
- re-establishment of continuity  

### Validated operational conclusion

This case demonstrates that:

- any platform without bounded-time recovery is non-admissible  
- centralized dependency creates structural risk  
- absence of appeal or re-entry is sufficient to reject the system  
- recoverability constraints require multi-platform redundancy  

---

## Case 3 — Medical Result Communication Delay or Misreporting

### Case summary
A patient requires a diagnostic test result for clinical decision-making.

The test is performed, but:

- the result is not delivered in time, or
- the result is communicated incorrectly (e.g., by non-clinical staff), or
- access to the result is delayed or blocked

### System state

System components:

- patient
- laboratory system
- communication interface (receptionist / phone / report system)
- clinical decision pathway

Observed issues:

- result exists but is not accessible in time
- communication is mediated by non-authoritative channel
- no guarantee of accuracy in transmission

### Boundary evaluation

- Can the correct state be detected in time? → NO / UNKNOWN  
- Can action be taken in time? → NO  
- Can recovery occur if information is wrong? → NO  

### Failure classification

- communication delay
- information integrity failure
- dependency on non-clinical relay
- response blockage due to missing data

### Decision

- NON-ADMISSIBLE  

→ clinical decision must not proceed under uncertain or delayed result conditions  

### Required action

- direct access to verified result required  
- escalation to laboratory or clinician  
- bypass unreliable communication channel  

### Validated operational conclusion

This case demonstrates that:

- delay in critical information is equivalent to loss of detection  
- incorrect communication introduces unrecoverable risk  
- non-authoritative transmission channels are non-admissible  
- recoverability requires direct, verifiable access to clinical data in time

- ---

## Case 4 — Infrastructure Failure: Power Loss Without Recoverable Backup

### Case summary
A system dependent on continuous electrical power experiences an outage.

A backup system (generator, battery, or redundancy) is either:

- not present
- not activated in time
- insufficient to sustain required operation

### System state

System components:

- primary power source
- backup power system
- dependent system (device, infrastructure, or service)

Observed conditions:

- loss of primary power
- delayed or failed backup activation
- insufficient backup duration

### Boundary evaluation

- Can the system maintain operation in time? → NO  
- Can response occur before failure? → NO  
- Can recovery restore continuity in time? → NO  

### Failure classification

- infrastructure dependency failure  
- insufficient redundancy  
- response delay beyond recoverability window  
- continuity failure under load or outage  

### Decision

- NON-ADMISSIBLE  

→ system must not rely on this configuration for continuity-critical operation  

### Required action

- implement redundant, independent power sources  
- ensure automatic activation within required time  
- validate backup duration against worst-case scenarios  

### Validated operational conclusion

This case demonstrates that:

- backup systems must be executable in time, not just present  
- delayed activation is equivalent to absence  
- insufficient duration is equivalent to failure  
- infrastructure without guaranteed recoverability is non-admissible  
