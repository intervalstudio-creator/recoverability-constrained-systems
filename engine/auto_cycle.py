import threading, time
from datetime import datetime, timezone
from engine.event_bus import latest_event
from engine.execution_v2 import execute_case_v2
AUTO_STATE = {"running": False, "interval_seconds": 5, "last_run_utc": None, "last_status": None}
_thread = None
def _loop():
    while AUTO_STATE["running"]:
        event = latest_event()
        if event:
            AUTO_STATE["last_status"] = execute_case_v2(event)
            AUTO_STATE["last_run_utc"] = datetime.now(timezone.utc).isoformat()
        time.sleep(AUTO_STATE["interval_seconds"])
def start_auto_cycle(interval_seconds: int = 5):
    global _thread
    if AUTO_STATE["running"]:
        return AUTO_STATE
    AUTO_STATE["running"] = True
    AUTO_STATE["interval_seconds"] = interval_seconds
    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()
    return AUTO_STATE
def stop_auto_cycle():
    AUTO_STATE["running"] = False
    return AUTO_STATE
def get_auto_state():
    return AUTO_STATE
