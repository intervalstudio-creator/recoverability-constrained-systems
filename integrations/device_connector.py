from integrations.webhook_connector import send_webhook
def trigger_device(endpoint_url: str, action: str, metadata: dict | None = None):
    return {"ok": True, "channel": "device", "response": send_webhook(endpoint_url, {"event":"boundary.device.action","action":action,"metadata":metadata or {}})}
