import json, pathlib, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.runtime_store import get_state, set_mode, add_telemetry
from engine.observability import get_observability_snapshot
from engine.event_bus import publish_event, get_events
from engine.auto_cycle import start_auto_cycle, stop_auto_cycle, get_auto_state
from engine.execution_v2 import execute_case_v2


def evaluate_medication_case(data):
    reasons = []

    if not data.get("dose_known", False):
        reasons.append("DOSE_UNKNOWN")

    if not data.get("duration_known", False):
        reasons.append("DURATION_UNKNOWN")

    if not data.get("patient_state_known", False):
        reasons.append("STATE_UNKNOWN")

    if not data.get("co_medications_known", False):
        reasons.append("CO_MEDS_UNKNOWN")

    if not data.get("monitoring_present", False):
        reasons.append("MONITORING_ABSENT")

    if not data.get("access_continuity", False):
        reasons.append("ACCESS_INTERRUPTED")

    if not data.get("intervention_available", False):
        reasons.append("INTERVENTION_UNAVAILABLE")

    if not data.get("withdrawal_risk_bounded", False):
        reasons.append("RISK_NOT_BOUNDED")

    if not data.get("time_to_irreversibility_known", False):
        reasons.append("TIME_WINDOW_UNKNOWN")

    if not data.get("response_within_window", False):
        reasons.append("RESPONSE_TOO_LATE")

    if not data.get("recovery_path_exists", False):
        reasons.append("NO_RECOVERY_PATH")

    medication_class = data.get("medication_class", "benzodiazepine")

    if medication_class == "benzodiazepine":
        if not data.get("access_continuity", False):
            reasons.append("BENZO_ACCESS_BREAK")
        if not data.get("monitoring_present", False):
            reasons.append("BENZO_WITHDRAWAL_UNMONITORED")
        if not data.get("withdrawal_risk_bounded", False):
            reasons.append("BENZO_WITHDRAWAL_NOT_BOUNDED")
        if not data.get("recovery_path_exists", False):
            reasons.append("BENZO_NO_STABILIZATION_PATH")

    reasons = sorted(set(reasons))

    can_execute_protective_action = (
        data.get("intervention_available", False)
        and data.get("response_within_window", False)
        and data.get("time_to_irreversibility_known", False)
    )

    if len(reasons) == 0:
        return {
            "case_type": data.get("case_type", "medication_withdrawal"),
            "medication_class": medication_class,
            "decision": "CONTINUE",
            "admissible": True,
            "action": "CONTINUE_WITH_MONITORING",
            "reasons": []
        }

    if can_execute_protective_action:
        return {
            "case_type": data.get("case_type", "medication_withdrawal"),
            "medication_class": medication_class,
            "decision": "STOP",
            "admissible": False,
            "action": "STABILIZE_ESCALATE_CONTAIN",
            "reasons": reasons
        }

    return {
        "case_type": data.get("case_type", "medication_withdrawal"),
        "medication_class": medication_class,
        "decision": "NON-EXECUTABLE",
        "admissible": False,
        "action": "EMERGENCY_NON_EXECUTABLE_STATE",
        "reasons": reasons
    }


class Handler(BaseHTTPRequestHandler):
    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _write_json(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/runtime-status":
            self._write_json(200, get_state())
        elif self.path == "/api/observability":
            self._write_json(200, get_observability_snapshot())
        elif self.path == "/api/events":
            self._write_json(200, {"events": get_events()})
        elif self.path == "/api/auto/status":
            self._write_json(200, get_auto_state())
        else:
            self._write_json(404, {"error": "not_found"})

    def do_POST(self):
        if self.path == "/api/runtime/modes":
            payload = self._read_json()
            set_mode(payload.get("mode", "online"))
            self._write_json(200, {"ok": True, "mode": get_state()["mode"]})

        elif self.path == "/api/runtime/telemetry":
            payload = self._read_json()
            add_telemetry(payload)
            self._write_json(200, {"ok": True, "event_count": len(get_state()["telemetry_events"])})

        elif self.path == "/api/events":
            payload = self._read_json()
            event = publish_event(payload)
            self._write_json(200, {"event": event, "result": execute_case_v2(event)})

        elif self.path == "/api/medication/evaluate":
            payload = self._read_json()
            result = evaluate_medication_case(payload)
            self._write_json(200, result)

        elif self.path == "/api/auto/start":
            payload = self._read_json()
            self._write_json(200, start_auto_cycle(int(payload.get("interval_seconds", 5))))

        elif self.path == "/api/auto/stop":
            self._write_json(200, stop_auto_cycle())

        else:
            self._write_json(404, {"error": "not_found"})


def run():
    server = HTTPServer(("127.0.0.1", 8787), Handler)
    print("Boundary server running on http://127.0.0.1:8787")
    server.serve_forever()


if __name__ == "__main__":
    run()
