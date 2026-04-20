import json
import os
from datetime import datetime, timezone

DEAD_LETTER_PATH = "audit/logs/dead_letter_queue.jsonl"

def enqueue_dead_letter(channel: str, payload: dict, error: str):
    os.makedirs(os.path.dirname(DEAD_LETTER_PATH), exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "payload": payload,
        "error": error,
        "status": "queued"
    }
    with open(DEAD_LETTER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
