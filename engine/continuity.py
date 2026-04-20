import json
from pathlib import Path

FLOOR_PATH = Path("configs/continuity/continuity_floors.json")

def get_continuity_floor(domain: str):
    data = json.loads(FLOOR_PATH.read_text(encoding="utf-8"))
    return data.get(domain, data.get("generic", {}))
