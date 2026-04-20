import json
import os
from engine.health import get_health

ACTION_STATUS_PATH = "audit/logs/action_status.json"

def write_action_status(status: dict):
    os.makedirs(os.path.dirname(ACTION_STATUS_PATH), exist_ok=True)
    with open(ACTION_STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)

def get_observability_snapshot():
    action_status = {}
    if os.path.exists(ACTION_STATUS_PATH):
        with open(ACTION_STATUS_PATH, "r", encoding="utf-8") as f:
            action_status = json.load(f)
    return {
        "channel_health": get_health(),
        "last_action_status": action_status
    }
