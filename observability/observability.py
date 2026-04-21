"""
Boundary Observability v4.0
Full decision trace, residue logging, timeline reconstruction, incident library.
"""

import json
import os
import uuid
import time
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(os.environ.get("BOUNDARY_LOG_DIR", "./logs"))
LOG_DIR.mkdir(exist_ok=True)

DECISION_LOG_FILE  = LOG_DIR / "decisions.jsonl"
RESIDUE_LOG_FILE   = LOG_DIR / "residue.jsonl"
INCIDENT_LOG_FILE  = LOG_DIR / "incidents.jsonl"
OVERRIDE_LOG_FILE  = LOG_DIR / "overrides.jsonl"


def _append(filepath: Path, record: dict):
    with open(filepath, "a") as f:
        f.write(json.dumps(record, default=str) + "\n")


def _read_all(filepath: Path) -> list[dict]:
    if not filepath.exists():
        return []
    records = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


# ─────────────────────────────────────────────
# Decision Logging
# ─────────────────────────────────────────────

def log_decision(evaluation_result: dict):
    """Log a completed evaluation to the decision log."""
    record = {
        "log_type": "decision",
        "logged_at": datetime.now(timezone.utc).isoformat(),
        **evaluation_result,
    }
    _append(DECISION_LOG_FILE, record)


def get_decisions(domain: str = None, state: str = None, limit: int = 100) -> list[dict]:
    records = _read_all(DECISION_LOG_FILE)
    if domain:
        records = [r for r in records if r.get("domain") == domain]
    if state:
        records = [r for r in records if r.get("boundary_state") == state]
    return records[-limit:]


# ─────────────────────────────────────────────
# Residue Logging
# ─────────────────────────────────────────────

def log_residue(case_id: str, residue_type: str, description: str, metadata: dict = None):
    """
    Log unresolved structural residue — prior failures, deferred corrections,
    non-recoverable losses, unanswered escalations.
    """
    record = {
        "log_type": "residue",
        "residue_id": str(uuid.uuid4()),
        "case_id": case_id,
        "residue_type": residue_type,
        "description": description,
        "metadata": metadata or {},
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "resolved": False,
    }
    _append(RESIDUE_LOG_FILE, record)
    return record["residue_id"]


def resolve_residue(residue_id: str, resolved_by: str, resolution_note: str):
    """Mark a residue entry as resolved."""
    records = _read_all(RESIDUE_LOG_FILE)
    updated = []
    for r in records:
        if r.get("residue_id") == residue_id:
            r["resolved"] = True
            r["resolved_by"] = resolved_by
            r["resolved_at"] = datetime.now(timezone.utc).isoformat()
            r["resolution_note"] = resolution_note
        updated.append(r)
    with open(RESIDUE_LOG_FILE, "w") as f:
        for r in updated:
            f.write(json.dumps(r, default=str) + "\n")


def get_unresolved_residue() -> list[dict]:
    return [r for r in _read_all(RESIDUE_LOG_FILE) if not r.get("resolved")]


# ─────────────────────────────────────────────
# Override Accountability
# ─────────────────────────────────────────────

def log_override(case_id: str, operator_id: str, reason: str, original_state: str):
    """
    Log every override. Identity, reason, timing, and residue are all recorded.
    An override without attribution is itself a boundary violation.
    """
    record = {
        "log_type": "override",
        "override_id": str(uuid.uuid4()),
        "case_id": case_id,
        "operator_id": operator_id,
        "reason": reason,
        "original_state": original_state,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _append(OVERRIDE_LOG_FILE, record)
    # Auto-log residue for every override
    log_residue(case_id, "override_residue", f"Override by {operator_id}: {reason}", metadata=record)
    return record["override_id"]


def get_overrides(case_id: str = None) -> list[dict]:
    records = _read_all(OVERRIDE_LOG_FILE)
    if case_id:
        records = [r for r in records if r.get("case_id") == case_id]
    return records


# ─────────────────────────────────────────────
# Incident Library
# ─────────────────────────────────────────────

def save_incident(evaluation_result: dict, notes: str = ""):
    """Save a real case to the searchable incident library."""
    record = {
        "log_type": "incident",
        "incident_id": str(uuid.uuid4()),
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "notes": notes,
        **evaluation_result,
    }
    _append(INCIDENT_LOG_FILE, record)
    return record["incident_id"]


def search_incidents(domain: str = None, state: str = None, text: str = None) -> list[dict]:
    records = _read_all(INCIDENT_LOG_FILE)
    if domain:
        records = [r for r in records if r.get("domain") == domain]
    if state:
        records = [r for r in records if r.get("boundary_state") == state]
    if text:
        text_lower = text.lower()
        records = [r for r in records if text_lower in json.dumps(r).lower()]
    return records


# ─────────────────────────────────────────────
# Timeline Reconstruction
# ─────────────────────────────────────────────

def reconstruct_timeline(case_id: str) -> dict:
    """
    Reconstruct the full timeline for a case_id:
    when boundary was crossed, when escalation was triggered, overrides.
    """
    decisions = [r for r in _read_all(DECISION_LOG_FILE) if r.get("case_id") == case_id]
    overrides = get_overrides(case_id)
    residues  = [r for r in _read_all(RESIDUE_LOG_FILE) if r.get("case_id") == case_id]

    events = []
    for d in decisions:
        events.append({"type": "decision", "state": d.get("boundary_state"), "timestamp": d.get("timestamp"), "detail": d})
    for o in overrides:
        events.append({"type": "override", "timestamp": o.get("timestamp"), "detail": o})
    for r in residues:
        events.append({"type": "residue", "resolved": r.get("resolved"), "timestamp": r.get("logged_at"), "detail": r})

    events.sort(key=lambda e: e.get("timestamp", ""))

    # Find first non-admissible crossing
    first_non_admissible = next(
        (e for e in events if e.get("type") == "decision" and e["state"] in ["NON-ADMISSIBLE", "NON-EXECUTABLE"]),
        None
    )

    return {
        "case_id": case_id,
        "total_events": len(events),
        "timeline": events,
        "first_non_admissible_at": first_non_admissible["timestamp"] if first_non_admissible else None,
        "override_count": len(overrides),
        "unresolved_residue_count": len([r for r in residues if not r.get("resolved")]),
    }


# ─────────────────────────────────────────────
# Dashboard Summary
# ─────────────────────────────────────────────

def get_dashboard_summary() -> dict:
    """Return a cross-domain dashboard snapshot."""
    decisions = _read_all(DECISION_LOG_FILE)
    residues  = _read_all(RESIDUE_LOG_FILE)
    overrides = _read_all(OVERRIDE_LOG_FILE)

    recent = sorted(decisions, key=lambda r: r.get("timestamp", ""), reverse=True)[:50]

    by_state = {}
    by_domain = {}
    for r in recent:
        s = r.get("boundary_state", "UNKNOWN")
        d = r.get("domain", "unknown")
        by_state[s] = by_state.get(s, 0) + 1
        by_domain[d] = by_domain.get(d, 0) + 1

    non_admissible_recent = [r for r in recent if r.get("boundary_state") in ["NON-ADMISSIBLE", "NON-EXECUTABLE"]]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_decisions": len(decisions),
        "total_overrides": len(overrides),
        "total_residue": len(residues),
        "unresolved_residue": len([r for r in residues if not r.get("resolved")]),
        "recent_by_state": by_state,
        "recent_by_domain": by_domain,
        "recent_non_admissible": non_admissible_recent[:10],
        "recent_decisions": recent[:10],
    }
