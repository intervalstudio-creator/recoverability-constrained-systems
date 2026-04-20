from collections import deque
from datetime import datetime, timezone
EVENTS = deque(maxlen=500)
def publish_event(event: dict):
    payload = dict(event)
    payload["received_at_utc"] = datetime.now(timezone.utc).isoformat()
    EVENTS.append(payload)
    return payload
def get_events():
    return list(EVENTS)
def latest_event():
    return EVENTS[-1] if EVENTS else None
