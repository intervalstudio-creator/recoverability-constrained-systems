"""
Public Boundary evaluation surface.

This public version intentionally exposes only high-level admissibility logic.
Detailed thresholds, timing mechanics, and optimization internals are withheld.
"""

from enum import Enum


class BoundaryState(str, Enum):
    CONTINUE = "CONTINUE"
    DEGRADED = "DEGRADED"
    NON_ADMISSIBLE = "NON-ADMISSIBLE"
    NON_EXECUTABLE = "NON-EXECUTABLE"


PUBLIC_DOMAINS = [
    "pharmacological",
    "healthcare",
    "identity",
    "finance",
    "housing",
    "legal",
    "labour",
    "education",
    "infrastructure",
    "disaster",
    "transport",
    "supply_chain",
    "energy",
    "communications",
    "food_water",
]


def evaluate_public_case(case: dict) -> dict:
    """
    High-level public evaluator.

    Inputs are reduced to public-safe recoverability signals:
    - whether a recovery path is visible
    - whether detection is possible
    - whether response is possible
    - whether execution remains feasible
    """
    recovery_path = bool(case.get("recovery_path_exists"))
    detection = bool(case.get("failure_detectable"))
    response = bool(case.get("response_possible"))
    execution_window = bool(case.get("execution_window_open", True))

    missing = []
    if not recovery_path:
        missing.append("RECOVERY_PATH_UNESTABLISHED")
    if not detection:
        missing.append("DETECTION_UNESTABLISHED")
    if not response:
        missing.append("RESPONSE_UNESTABLISHED")

    if not execution_window:
        state = BoundaryState.NON_EXECUTABLE.value
    elif missing:
        state = BoundaryState.NON_ADMISSIBLE.value
    elif case.get("degraded_margin"):
        state = BoundaryState.DEGRADED.value
    else:
        state = BoundaryState.CONTINUE.value

    return {
        "state": state,
        "domain": case.get("domain", "unknown"),
        "failed_checks": missing,
        "summary": "Public admissibility output only. Detailed execution mechanics are withheld.",
    }
