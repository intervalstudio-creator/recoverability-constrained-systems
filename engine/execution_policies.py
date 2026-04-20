def build_execution_policy(decision: str, domain: str, event_type: str = None):
    base = {"decision":decision,"domain":domain,"event_type":event_type,"require_human_ack":False,"continuity_floor_required":False,"channels":[],"device_action":None}
    if decision == "HALT":
        base["channels"] = ["email","sms","incident","webhook"]
        base["continuity_floor_required"] = True
        if domain in {"identity","finance","healthcare","transport","disaster","infrastructure"}:
            base["device_action"] = "restrict_or_shutdown_unsafe_path"
    elif decision == "ESCALATE":
        base["channels"] = ["email","incident","webhook"]
        base["continuity_floor_required"] = True
        base["require_human_ack"] = True
    elif decision in {"RESTRICT","CONTAIN"}:
        base["channels"] = ["email","webhook"]
        base["continuity_floor_required"] = True
        base["device_action"] = "limit_exposure"
    return base
