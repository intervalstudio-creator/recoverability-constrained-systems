def evaluate(case: dict):
    reasons = []

    if not case.get("boundary_detectable", False):
        reasons.append("Boundary cannot be detected in time")
        return {"decision": "HALT", "reasons": reasons}

    if not case.get("response_possible_in_time", False):
        reasons.append("Response cannot occur within recoverability window")
        return {"decision": "HALT", "reasons": reasons}

    if not case.get("recovery_path_verified", False):
        reasons.append("Recovery path not verified under real conditions")
        return {"decision": "HALT", "reasons": reasons}

    if case.get("critical_unknowns_present", False):
        reasons.append("Unknown continuity-critical conditions present")
        return {"decision": "HALT", "reasons": reasons}

    if case.get("dependency_unavailable", False):
        reasons.append("Required dependency unavailable within time")
        return {"decision": "ESCALATE", "reasons": reasons}

    reasons.append("Recoverability established in time under real conditions")
    return {"decision": "CONTINUE", "reasons": reasons}
