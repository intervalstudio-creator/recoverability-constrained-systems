function evaluateMedicationPublic(input) {
  const reasons = [];

  if (!input.access_continuity) reasons.push("ACCESS_INTERRUPTED");
  if (!input.monitoring_present) reasons.push("MONITORING_ABSENT");
  if (!input.recovery_path_exists) reasons.push("RECOVERY_PATH_UNESTABLISHED");
  if (!input.response_possible) reasons.push("RESPONSE_UNAVAILABLE");

  let decision = "CONTINUE";

  if (input.execution_window_open === false) {
    decision = "NON-EXECUTABLE";
  } else if (reasons.length) {
    decision = "NON-ADMISSIBLE";
  } else if (input.degraded_margin) {
    decision = "DEGRADED";
  }

  return {
    case_type: input.case_type || "medication_continuity",
    decision,
    reasons,
    note: "Public medication checks are intentionally simplified. Detailed clinical timing and intervention pathways are withheld."
  };
}

if (typeof module !== "undefined") {
  module.exports = { evaluateMedicationPublic };
}
