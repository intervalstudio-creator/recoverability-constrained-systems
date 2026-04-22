from datetime import datetime, timezone


def log_event(action, user):
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} | {user} | {action}\n")
