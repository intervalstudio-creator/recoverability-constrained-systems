function unique(arr) {
  return [...new Set(arr)];
}

function classifyMedicationClass(input) {
  return input.medication_class || "benzodiazepine";
}

function applyGenericChecks(input, reasons) {
  if (!input.dose_known) reasons.push("DOSE_UNKNOWN");
  if (!input.duration_known) reasons.push("DURATION_UNKNOWN");
  if (!input.patient_state_known) reasons.push("STATE_UNKNOWN");
  if (!input.co_medications_known) reasons.push("CO_MEDS_UNKNOWN");
  if (!input.monitoring_present) reasons.push("MONITORING_ABSENT");
  if (!input.access_continuity) reasons.push("ACCESS_INTERRUPTED");
  if (!input.intervention_available) reasons.push("INTERVENTION_UNAVAILABLE");
  if (!input.withdrawal_risk_bounded) reasons.push("RISK_NOT_BOUNDED");
  if (!input.time_to_irreversibility_known) reasons.push("TIME_WINDOW_UNKNOWN");
  if (!input.response_within_window) reasons.push("RESPONSE_TOO_LATE");
  if (!input.recovery_path_exists) reasons.push("NO_RECOVERY_PATH");
  if (!input.substitution_verified && input.substitution_attempted) reasons.push("SUBSTITUTION_UNVERIFIED");
}

function applyClassSpecificChecks(input, reasons) {
  const cls = classifyMedicationClass(input);

  if (cls === "benzodiazepine") {
    if (!input.access_continuity) reasons.push("BENZO_ACCESS_BREAK");
    if (!input.monitoring_present) reasons.push("BENZO_WITHDRAWAL_UNMONITORED");
    if (!input.withdrawal_risk_bounded) reasons.push("BENZO_WITHDRAWAL_NOT_BOUNDED");
    if (!input.recovery_path_exists) reasons.push("BENZO_NO_STABILIZATION_PATH");
  }

  if (cls === "acute") {
    if (!input.access_continuity) reasons.push("ACUTE_THERAPY_INTERRUPTED");
    if (!input.response_within_window) reasons.push("ACUTE_RESPONSE_WINDOW_MISSED");
  }

  if (cls === "balance") {
    if (!input.monitoring_present) reasons.push("BALANCE_SYSTEM_UNMONITORED");
  }

  if (cls === "polypharmacy") {
    if (!input.co_medications_known) reasons.push("POLYPHARMACY_INTERACTION_UNKNOWN");
  }
}

function evaluateMedication(input) {
  let reasons = [];
  applyGenericChecks(input, reasons);
  applyClassSpecificChecks(input, reasons);
  reasons = unique(reasons);

  const canExecuteProtectiveAction =
    !!input.intervention_available &&
    !!input.response_within_window &&
    !!input.time_to_irreversibility_known;

  let decision = "CONTINUE";
  let action = "CONTINUE_WITH_MONITORING";

  if (reasons.length > 0 && canExecuteProtectiveAction) {
    decision = "STOP";
    action = "STABILIZE_ESCALATE_CONTAIN";
  } else if (reasons.length > 0 && !canExecuteProtectiveAction) {
    decision = "NON-EXECUTABLE";
    action = "EMERGENCY_NON_EXECUTABLE_STATE";
  }

  return {
    case_type: input.case_type || "medication_withdrawal",
    medication_class: classifyMedicationClass(input),
    admissible: decision === "CONTINUE",
    decision,
    action,
    reasons
  };
}

function medicationPresetBenzoFailure() {
  return {
    case_type: "medication_withdrawal",
    medication_class: "benzodiazepine",
    dose_known: true,
    duration_known: true,
    patient_state_known: false,
    co_medications_known: false,
    monitoring_present: false,
    access_continuity: false,
    intervention_available: true,
    withdrawal_risk_bounded: false,
    time_to_irreversibility_known: true,
    response_within_window: true,
    recovery_path_exists: false,
    substitution_attempted: false,
    substitution_verified: false
  };
}
