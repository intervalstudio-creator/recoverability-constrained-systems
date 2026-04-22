import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

FILE = DATA_DIR / "records.json"


def load_records():
    if not FILE.exists():
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_record(record):
    records = load_records()
    records.append(record)
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
