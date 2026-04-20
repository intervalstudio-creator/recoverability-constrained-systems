from datetime import datetime, timezone
CHANNEL_HEALTH = {
    "email": {"status": "unknown", "last_success": None, "last_failure": None},
    "sms": {"status": "unknown", "last_success": None, "last_failure": None},
    "incident": {"status": "unknown", "last_success": None, "last_failure": None},
    "webhook": {"status": "unknown", "last_success": None, "last_failure": None},
    "device": {"status": "unknown", "last_success": None, "last_failure": None},
}
def _now():
    return datetime.now(timezone.utc).isoformat()
def mark_success(channel: str):
    CHANNEL_HEALTH.setdefault(channel, {})
    CHANNEL_HEALTH[channel]["status"] = "healthy"
    CHANNEL_HEALTH[channel]["last_success"] = _now()
def mark_failure(channel: str, error: str):
    CHANNEL_HEALTH.setdefault(channel, {})
    CHANNEL_HEALTH[channel]["status"] = "degraded"
    CHANNEL_HEALTH[channel]["last_failure"] = _now()
    CHANNEL_HEALTH[channel]["last_error"] = error
def get_health():
    return CHANNEL_HEALTH
