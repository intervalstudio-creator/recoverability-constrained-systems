from boundary_agent import RCCSInput, evaluate

def evaluate_message(
    state_visible: bool,
    time_to_irreversibility: float,
    time_to_detection: float,
    time_to_response: float,
    time_to_recovery: float,
    dependencies_ok: bool,
    challengeable: bool,
    correctable: bool,
) -> str:
    return evaluate(RCCSInput(
        state_visible=state_visible,
        time_to_irreversibility=time_to_irreversibility,
        time_to_detection=time_to_detection,
        time_to_response=time_to_response,
        time_to_recovery=time_to_recovery,
        dependencies_ok=dependencies_ok,
        challengeable=challengeable,
        correctable=correctable,
    ))
