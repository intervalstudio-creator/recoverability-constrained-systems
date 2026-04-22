function evaluateBoundaryPublic(input) {
  const failed = [];

  if (!input.recovery_path_exists) failed.push("RECOVERY_PATH_UNESTABLISHED");
  if (!input.failure_detectable) failed.push("DETECTION_UNESTABLISHED");
  if (!input.response_possible) failed.push("RESPONSE_UNESTABLISHED");

  let state = "CONTINUE";

  if (input.execution_window_open === false) {
    state = "NON-EXECUTABLE";
  } else if (failed.length > 0) {
    state = "NON-ADMISSIBLE";
  } else if (input.degraded_margin) {
    state = "DEGRADED";
  }

  return {
    state,
    failed_checks: failed,
    note: "Public evaluation output only. Detailed thresholds and orchestration are intentionally excluded."
  };
}

if (typeof module !== "undefined") {
  module.exports = { evaluateBoundaryPublic };
}
