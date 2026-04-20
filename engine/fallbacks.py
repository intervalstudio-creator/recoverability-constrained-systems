import json
from pathlib import Path

FALLBACK_PATH = Path("configs/profiles/default_fallbacks.json")

def get_fallbacks():
    return json.loads(FALLBACK_PATH.read_text(encoding="utf-8"))

def resolve_fallbacks(domain: str):
    data = get_fallbacks()
    if domain == "healthcare":
        return data.get("transport", []) + data.get("communications", [])
    return data.get(domain, []) or data.get("compute", [])
