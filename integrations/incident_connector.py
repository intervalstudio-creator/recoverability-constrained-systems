import requests
from engine.config import get_env
from engine.retry import with_retry

def create_incident(title: str, description: str, severity: str = "critical"):
    routing_key = get_env("BOUNDARY_PAGERDUTY_ROUTING_KEY")
    if not routing_key:
        raise RuntimeError("Incident provider not configured")

    payload = {
        "routing_key": routing_key,
        "event_action": "trigger",
        "payload": {
            "summary": title,
            "severity": severity,
            "source": "boundary",
            "custom_details": {"description": description}
        }
    }

    def _send():
        r = requests.post("https://events.pagerduty.com/v2/enqueue", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()

    resp = with_retry(_send, retriable_exceptions=(requests.RequestException,))
    return {"ok": True, "channel": "incident", "provider_response": resp}
