import json
import os
from datetime import datetime, timezone
from engine.config import get_env

def write_audit_record(channel: str, status: str, payload: dict, metadata: dict | None = None):
    path = get_env("BOUNDARY_AUDIT_LOG_PATH", "audit/logs/external_actions.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "status": status,
        "payload": payload,
        "metadata": metadata or {}
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
