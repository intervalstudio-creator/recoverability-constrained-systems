import json
from pathlib import Path

AUTHORITY_PATH = Path("configs/authority/default_chain.json")

def get_authority_chain():
    return json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))["chain"]

def route_authority(decision: str):
    chain = get_authority_chain()
    if decision == "CONTINUE":
        return []
    return chain
