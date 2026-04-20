from integrations.email_connector import send_email
from integrations.sms_connector import send_sms
from integrations.webhook_connector import send_webhook
from integrations.incident_connector import create_incident
from integrations.device_connector import trigger_device
from engine.health import mark_success, mark_failure
from engine.dead_letter import enqueue_dead_letter
from engine.policy import get_channels_for_decision
from engine.observability import write_action_status
from engine.audit import write_audit_record

def execute_action_observed(decision: str, context: dict):
    outputs, attempted, failed = [], [], []
    for channel in get_channels_for_decision(decision):
        try:
            if channel == "email" and context.get("email"):
                outputs.append(send_email(context["email"], f"Boundary {decision}", context.get("email_body", f"Decision: {decision}"))); attempted.append("email"); mark_success("email")
            elif channel == "sms" and context.get("phone"):
                outputs.append(send_sms(context["phone"], context.get("sms_body", f"Decision: {decision}"))); attempted.append("sms"); mark_success("sms")
            elif channel == "incident" and context.get("incident_title"):
                outputs.append(create_incident(context["incident_title"], context.get("incident_description", f"Decision: {decision}"))); attempted.append("incident"); mark_success("incident")
            elif channel == "webhook" and context.get("webhook"):
                outputs.append(send_webhook(context["webhook"], {"event":"boundary.execution.decision","decision":decision,"context":context.get("webhook_context",{})})); attempted.append("webhook"); mark_success("webhook")
            elif channel == "device" and context.get("device_endpoint") and context.get("device_action"):
                outputs.append(trigger_device(context["device_endpoint"], context["device_action"], {"decision":decision})); attempted.append("device"); mark_success("device")
        except Exception as e:
            failed.append({"channel": channel, "error": str(e)})
            mark_failure(channel, str(e))
            enqueue_dead_letter(channel, {"decision": decision, "context": context}, str(e))
    status = {"decision": decision, "attempted_channels": attempted, "failed_channels": failed, "output_count": len(outputs), "ok": len(failed) == 0}
    write_action_status(status)
    write_audit_record("orchestrator", "executed", status)
    return status
