from uuid import uuid4
from engine.execution_layer import run_cycle
from engine.execution_policies import build_execution_policy
from engine.continuity_workflows import execute_continuity_workflow
from engine.external_actuation_observed import execute_action_observed
from engine.audit import write_audit_record

def normalize_event_to_case(event: dict):
    return {
        "domain": event.get("domain","general"),
        "boundary_detectable": event.get("boundary_detectable", True),
        "response_possible_in_time": event.get("response_possible_in_time", False),
        "recovery_path_verified": event.get("recovery_path_verified", False),
        "critical_unknowns_present": event.get("critical_unknowns_present", True),
        "dependency_unavailable": event.get("dependency_unavailable", False)
    }

def build_actuation_context(event: dict, policy: dict, case_id: str):
    return {
        "email": event.get("email",""),
        "phone": event.get("phone",""),
        "incident_title": event.get("incident_title", f"Boundary {policy['decision']}"),
        "incident_description": event.get("incident_description", f"Autonomous execution decision for case {case_id}"),
        "webhook": event.get("webhook",""),
        "webhook_context": {"domain": event.get("domain"), "event_type": event.get("event_type"), "source": "boundary.execution.v3.2", "case_id": case_id},
        "device_endpoint": event.get("device_endpoint",""),
        "device_action": policy.get("device_action")
    }

def execute_case_v2(event: dict):
    case_id = event.get("case_id") or str(uuid4())
    case = normalize_event_to_case(event)
    cycle = run_cycle(case)
    policy = build_execution_policy(cycle["decision"], case["domain"], event.get("event_type"))
    continuity = execute_continuity_workflow(case["domain"], case_id) if policy["continuity_floor_required"] else None
    actuation = execute_action_observed(cycle["decision"], build_actuation_context(event, policy, case_id))
    result = {"case_id": case_id, "cycle": cycle, "policy": policy, "continuity": continuity, "actuation": actuation}
    write_audit_record("execution_v2", "completed", {"case_id": case_id, "decision": cycle["decision"], "domain": case["domain"]})
    return result
