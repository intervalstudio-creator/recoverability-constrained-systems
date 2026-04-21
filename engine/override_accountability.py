"""
Boundary — Override Accountability Record

When an institution or operator continues despite NON-ADMISSIBLE
or NON-EXECUTABLE conditions, every element of that decision is
recorded in a structured, tamper-evident format.

This is the accountability gap: continuation under constraint is
usually undocumented. When things go wrong, there is no trail.

This module produces records usable in:
  - Regulatory review
  - Legal proceedings
  - Institutional learning
  - Incident investigation

Equivalent to a flight data recorder for decisions made under constraint.
"""

import uuid
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

OVERRIDE_RECORD_DIR = Path("./logs/override_records")
OVERRIDE_RECORD_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# Override Record
# ─────────────────────────────────────────────

def create_override_record(
    case_id:          str,
    domain:           str,
    boundary_state:   str,
    operator_id:      str,
    operator_role:    str,
    reason:           str,
    acknowledged_risk: str,
    authorising_authority: str,
    evaluation_result: dict,
    metadata:         dict = None,
) -> dict:
    """
    Create a fully attributed override record.

    All fields are mandatory. An override without full attribution
    is itself a boundary violation — this function enforces that.
    """
    record_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # Validate mandatory attribution fields
    missing = []
    if not operator_id:           missing.append("operator_id")
    if not operator_role:         missing.append("operator_role")
    if not reason:                missing.append("reason")
    if not acknowledged_risk:     missing.append("acknowledged_risk")
    if not authorising_authority: missing.append("authorising_authority")

    if missing:
        raise ValueError(
            f"Override record incomplete. Missing mandatory fields: {missing}. "
            f"An override without full attribution is a boundary violation."
        )

    record = {
        "record_id":             record_id,
        "record_type":           "OVERRIDE_ACCOUNTABILITY_RECORD",
        "version":               "1.0",
        "created_at":            timestamp,

        # Case identification
        "case_id":               case_id,
        "domain":                domain,
        "boundary_state_at_override": boundary_state,

        # Attribution (all mandatory)
        "operator_id":           operator_id,
        "operator_role":         operator_role,
        "authorising_authority": authorising_authority,

        # Decision record
        "reason_for_continuation": reason,
        "acknowledged_risk":     acknowledged_risk,

        # Context
        "evaluation_result":     evaluation_result,
        "metadata":              metadata or {},

        # Integrity
        "integrity_hash": None,  # filled below
    }

    # Compute integrity hash so record cannot be silently altered
    record_str = json.dumps(
        {k: v for k, v in record.items() if k != "integrity_hash"},
        sort_keys=True, default=str
    )
    record["integrity_hash"] = hashlib.sha256(record_str.encode()).hexdigest()

    # Persist to disk
    filepath = OVERRIDE_RECORD_DIR / f"{record_id}.json"
    with open(filepath, "w") as f:
        json.dump(record, f, indent=2, default=str)

    return record


def verify_record_integrity(record: dict) -> dict:
    """Verify that an override record has not been altered."""
    stored_hash = record.get("integrity_hash")
    recomputed_str = json.dumps(
        {k: v for k, v in record.items() if k != "integrity_hash"},
        sort_keys=True, default=str
    )
    recomputed_hash = hashlib.sha256(recomputed_str.encode()).hexdigest()
    intact = (stored_hash == recomputed_hash)
    return {
        "intact":           intact,
        "stored_hash":      stored_hash,
        "recomputed_hash":  recomputed_hash,
        "tampered":         not intact,
    }


def get_all_override_records(domain: str = None, operator_id: str = None) -> list[dict]:
    records = []
    for filepath in OVERRIDE_RECORD_DIR.glob("*.json"):
        try:
            with open(filepath) as f:
                r = json.load(f)
            if domain and r.get("domain") != domain:
                continue
            if operator_id and r.get("operator_id") != operator_id:
                continue
            records.append(r)
        except Exception:
            pass
    return sorted(records, key=lambda r: r.get("created_at", ""), reverse=True)


def generate_accountability_report(
    case_id: str = None,
    domain: str = None,
    from_date: str = None,
    to_date: str = None,
) -> dict:
    """
    Generate a formal accountability report — suitable for regulatory
    submission, legal proceedings, or institutional review.
    """
    records = get_all_override_records(domain=domain)
    if case_id:
        records = [r for r in records if r.get("case_id") == case_id]
    if from_date:
        records = [r for r in records if r.get("created_at", "") >= from_date]
    if to_date:
        records = [r for r in records if r.get("created_at", "") <= to_date]

    # Verify integrity of every record
    for r in records:
        r["_integrity"] = verify_record_integrity(r)

    tampered = [r for r in records if r["_integrity"]["tampered"]]
    by_state = {}
    by_domain = {}
    by_operator = {}

    for r in records:
        s = r.get("boundary_state_at_override", "UNKNOWN")
        d = r.get("domain", "unknown")
        o = r.get("operator_id", "unknown")
        by_state[s]    = by_state.get(s, 0) + 1
        by_domain[d]   = by_domain.get(d, 0) + 1
        by_operator[o] = by_operator.get(o, 0) + 1

    return {
        "report_id":           str(uuid.uuid4()),
        "generated_at":        datetime.now(timezone.utc).isoformat(),
        "report_type":         "OVERRIDE_ACCOUNTABILITY_REPORT",
        "filters_applied":     {"case_id": case_id, "domain": domain, "from_date": from_date, "to_date": to_date},
        "total_overrides":     len(records),
        "tampered_records":    len(tampered),
        "by_boundary_state":   by_state,
        "by_domain":           by_domain,
        "by_operator":         by_operator,
        "records":             records,
        "integrity_warning":   len(tampered) > 0,
    }
