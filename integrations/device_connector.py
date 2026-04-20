from integrations.webhook_connector import send_webhook

def trigger_device(endpoint_url: str, action: str, metadata: dict | None = None):
    payload = {
        "event": "boundary.device.action",
        "action": action,
        "metadata": metadata or {}
    }
    resp = send_webhook(endpoint_url, payload)
    return {"ok": True, "channel": "device", "response": resp}
