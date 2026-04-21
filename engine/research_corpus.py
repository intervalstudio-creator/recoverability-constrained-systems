"""
Boundary — Research Corpus

The incident library, when used at scale, becomes the first structured
dataset of recoverability failures across domains.

This module provides:
  - Structured corpus export for research
  - Pattern detection across incidents
  - Statistical summaries by domain, state, and timing
  - Anonymisation pipeline for research use
  - Export formats: JSON, CSV, and regulatory packs

This corpus has research value, policy value, and legal value.
"""

import csv
import json
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from collections import defaultdict

CORPUS_DIR = Path("./logs/corpus")
CORPUS_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# Anonymisation
# ─────────────────────────────────────────────

def anonymise_record(record: dict, salt: str = "boundary-research") -> dict:
    """
    Replace identifying fields with pseudonymous hashes.
    Preserves structural and timing information for research value.
    """
    def _hash(value: str) -> str:
        return hashlib.sha256(f"{salt}:{value}".encode()).hexdigest()[:16]

    anon = json.loads(json.dumps(record, default=str))  # deep copy

    # Hash identifying fields
    for field in ["case_id", "eval_id", "subject_id", "operator_id", "label"]:
        if field in anon and anon[field]:
            anon[field] = _hash(str(anon[field]))

    # Remove operator attribution details (keep domain, state, timing, rules)
    anon.pop("operator_role", None)
    anon.pop("authorising_authority", None)
    anon.pop("reason_for_continuation", None)
    anon.pop("acknowledged_risk", None)

    anon["_anonymised"] = True
    anon["_anonymised_at"] = datetime.now(timezone.utc).isoformat()
    return anon


# ─────────────────────────────────────────────
# Pattern Detection
# ─────────────────────────────────────────────

def detect_patterns(records: list[dict]) -> dict:
    """
    Detect failure patterns across a corpus of evaluation records.
    """
    if not records:
        return {"patterns": [], "summary": {}}

    # Most common failed conditions
    condition_failures: dict[str, int] = defaultdict(int)
    for r in records:
        for fc in r.get("failed_conditions", []):
            cid = fc.get("rule_id", fc.get("name", "unknown"))
            condition_failures[cid] += 1

    # Most common domain combinations in non-admissible cases
    non_admissible = [r for r in records if r.get("boundary_state") in ("NON-ADMISSIBLE", "NON-EXECUTABLE")]

    domain_frequency: dict[str, int] = defaultdict(int)
    for r in non_admissible:
        domain_frequency[r.get("domain", "unknown")] += 1

    # Timing patterns
    timing_records = [r for r in records if r.get("time_to_irreversibility")]
    avg_hours_at_non_admissible = None
    if timing_records:
        hours = [
            r["time_to_irreversibility"].get("hours_remaining", 0)
            for r in timing_records
            if r.get("boundary_state") in ("NON-ADMISSIBLE", "NON-EXECUTABLE")
            and r["time_to_irreversibility"].get("hours_remaining") is not None
        ]
        if hours:
            avg_hours_at_non_admissible = round(sum(hours) / len(hours), 2)

    # Escalation gap: cases where NON-EXECUTABLE was reached
    # (suggests escalation happened too late or not at all)
    non_executable_count = len([r for r in records if r.get("boundary_state") == "NON-EXECUTABLE"])
    escalation_gap_rate = round(non_executable_count / max(len(records), 1), 3)

    # Override rate: cases that had overrides
    override_count = len([r for r in records if r.get("override_active") or r.get("_override_record")])

    patterns = []

    # Pattern: most common single points of failure
    if condition_failures:
        top_failure = max(condition_failures, key=condition_failures.get)
        patterns.append({
            "pattern_id": "P001",
            "type": "single_point_failure",
            "description": f"Most common single failure condition: {top_failure} ({condition_failures[top_failure]} occurrences)",
            "frequency": condition_failures[top_failure],
            "affected_domain": "cross-domain",
        })

    # Pattern: escalation gap
    if escalation_gap_rate > 0.1:
        patterns.append({
            "pattern_id": "P002",
            "type": "escalation_gap",
            "description": f"{round(escalation_gap_rate * 100, 1)}% of cases reached NON-EXECUTABLE, suggesting late or absent escalation",
            "rate": escalation_gap_rate,
            "affected_domain": "cross-domain",
        })

    # Pattern: domain clustering
    if domain_frequency:
        top_domain = max(domain_frequency, key=domain_frequency.get)
        patterns.append({
            "pattern_id": "P003",
            "type": "domain_clustering",
            "description": f"Highest non-admissible rate in domain: {top_domain}",
            "domain": top_domain,
            "count": domain_frequency[top_domain],
        })

    return {
        "total_records_analysed": len(records),
        "non_admissible_count":   len(non_admissible),
        "non_executable_count":   non_executable_count,
        "escalation_gap_rate":    escalation_gap_rate,
        "avg_hours_at_non_admissible": avg_hours_at_non_admissible,
        "override_count":         override_count,
        "most_failed_conditions": dict(sorted(condition_failures.items(), key=lambda x: -x[1])[:10]),
        "non_admissible_by_domain": dict(sorted(domain_frequency.items(), key=lambda x: -x[1])),
        "patterns":               patterns,
    }


# ─────────────────────────────────────────────
# Export formats
# ─────────────────────────────────────────────

def export_corpus_json(records: list[dict], anonymise: bool = True, filepath: str = None) -> str:
    if anonymise:
        records = [anonymise_record(r) for r in records]

    export = {
        "corpus_id":      str(uuid.uuid4()),
        "exported_at":    datetime.now(timezone.utc).isoformat(),
        "anonymised":     anonymise,
        "total_records":  len(records),
        "schema_version": "1.0",
        "records":        records,
        "patterns":       detect_patterns(records),
    }

    if filepath:
        with open(filepath, "w") as f:
            json.dump(export, f, indent=2, default=str)
        return filepath

    path = CORPUS_DIR / f"corpus_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    with open(path, "w") as f:
        json.dump(export, f, indent=2, default=str)
    return str(path)


def export_corpus_csv(records: list[dict], anonymise: bool = True, filepath: str = None) -> str:
    if anonymise:
        records = [anonymise_record(r) for r in records]

    flat_records = []
    for r in records:
        tti = r.get("time_to_irreversibility") or {}
        flat = {
            "eval_id":          r.get("eval_id", ""),
            "case_id":          r.get("case_id", ""),
            "domain":           r.get("domain", ""),
            "boundary_state":   r.get("boundary_state", ""),
            "timestamp":        r.get("timestamp", ""),
            "failed_count":     r.get("failed_count", 0),
            "unknown_count":    r.get("unknown_count", 0),
            "total_rules":      r.get("total_rules_evaluated", 0),
            "hours_remaining":  tti.get("hours_remaining", ""),
            "ponr_crossed":     tti.get("point_of_no_return_crossed", ""),
        }
        flat_records.append(flat)

    path = filepath or str(CORPUS_DIR / f"corpus_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv")
    with open(path, "w", newline="") as f:
        if flat_records:
            writer = csv.DictWriter(f, fieldnames=flat_records[0].keys())
            writer.writeheader()
            writer.writerows(flat_records)

    return path


def generate_regulatory_pack(records: list[dict], domain: str = None) -> dict:
    """
    Generate a regulatory submission pack.
    Suitable for patient safety, medical device safety, operational risk,
    governance controls, and infrastructure resilience submissions.
    """
    if domain:
        records = [r for r in records if r.get("domain") == domain]

    patterns = detect_patterns(records)
    non_admissible = [r for r in records if r.get("boundary_state") in ("NON-ADMISSIBLE", "NON-EXECUTABLE")]

    return {
        "pack_id":           str(uuid.uuid4()),
        "generated_at":      datetime.now(timezone.utc).isoformat(),
        "pack_type":         "REGULATORY_SUBMISSION_PACK",
        "domain_filter":     domain or "all",
        "schema_version":    "1.0",
        "summary": {
            "total_evaluations":       len(records),
            "non_admissible_count":    len(non_admissible),
            "non_admissible_rate":     round(len(non_admissible) / max(len(records), 1), 3),
            "escalation_gap_rate":     patterns.get("escalation_gap_rate"),
            "most_failed_conditions":  patterns.get("most_failed_conditions"),
        },
        "patterns":           patterns["patterns"],
        "non_admissible_cases": [anonymise_record(r) for r in non_admissible[:100]],
        "regulatory_mappings": {
            "patient_safety":         "Boundary Protocol RC-001 through RC-006 map to patient safety critical criteria",
            "operational_risk":       "NON-ADMISSIBLE and NON-EXECUTABLE states correspond to operational risk thresholds",
            "governance_controls":    "Override accountability records map to governance control requirements",
            "infrastructure_resilience": "Degraded-mode and fallback-path evaluations map to resilience standards",
        },
    }
