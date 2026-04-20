from datetime import datetime, timezone
from engine.core import evaluate
from engine.authority import route_authority
from engine.fallbacks import resolve_fallbacks
from engine.continuity import get_continuity_floor
from engine.runtime_store import set_last_cycle

def run_cycle(case: dict):
    result = evaluate(case)
    domain = case.get("domain", "generic")

    cycle = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "case": case,
        "decision": result["decision"],
        "reasons": result["reasons"],
        "authority_route": route_authority(result["decision"]),
        "fallbacks": resolve_fallbacks(domain),
        "continuity_floor": get_continuity_floor(domain)
    }
    set_last_cycle(cycle)
    return cycle
