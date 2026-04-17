from dataclasses import dataclass

@dataclass
class RCCSInput:
    state_visible: bool
    time_to_irreversibility: float
    time_to_detection: float
    time_to_response: float
    time_to_recovery: float
    dependencies_ok: bool
    challengeable: bool
    correctable: bool

def evaluate(inp: RCCSInput) -> str:
    if not inp.state_visible:
        return "NON_ADMISSIBLE_DO_NOT_PROPAGATE"
    if not inp.dependencies_ok:
        return "NON_ADMISSIBLE_DO_NOT_PROPAGATE"
    if not inp.challengeable or not inp.correctable:
        return "NON_ADMISSIBLE_DO_NOT_PROPAGATE"
    total = inp.time_to_detection + inp.time_to_response + inp.time_to_recovery
    if total >= inp.time_to_irreversibility:
        return "NON_ADMISSIBLE_DO_NOT_PROPAGATE"
    return "ADMISSIBLE_TO_PROPAGATE"
