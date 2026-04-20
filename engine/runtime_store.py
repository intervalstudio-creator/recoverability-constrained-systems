from datetime import datetime, timezone

STATE = {
    "mode": "online",
    "telemetry_events": [],
    "last_cycle": None
}

def set_mode(mode: str):
    STATE["mode"] = mode

def add_telemetry(event: dict):
    event = dict(event)
    event["received_at_utc"] = datetime.now(timezone.utc).isoformat()
    STATE["telemetry_events"].append(event)
    STATE["telemetry_events"] = STATE["telemetry_events"][-200:]

def set_last_cycle(data: dict):
    STATE["last_cycle"] = data

def get_state():
    return STATE
