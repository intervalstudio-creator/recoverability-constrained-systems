"""
Boundary — Cross-Institutional Continuity Monitor

Treats a person or process as a continuity object across ALL domains
simultaneously. Detects when the combined state is non-admissible
even when no single institution has triggered an alert.

This is the visibility gap: each institution sees its own slice.
This module sees the whole picture.
"""

import uuid
from datetime import datetime, timezone
from typing import Any
from engine.boundary_engine import evaluate, BoundaryState, CROSS_DOMAIN_TRIGGERS


# ─────────────────────────────────────────────
# Continuity Object
# A person modelled across all active domains
# ─────────────────────────────────────────────

class ContinuityObject:
    """
    Represents a person or process as a multi-domain continuity object.
    Each domain holds its own state. The monitor evaluates all of them
    and computes a unified continuity status.
    """

    def __init__(self, subject_id: str, label: str = ""):
        self.subject_id   = subject_id
        self.label        = label or subject_id
        self.domains      = {}   # domain -> state dict
        self.history      = []   # list of full snapshots
        self.created_at   = datetime.now(timezone.utc).isoformat()

    def set_domain_state(self, domain: str, state: dict):
        self.domains[domain] = state

    def remove_domain(self, domain: str):
        self.domains.pop(domain, None)

    def to_dict(self) -> dict:
        return {
            "subject_id": self.subject_id,
            "label": self.label,
            "domains": self.domains,
            "created_at": self.created_at,
        }


# ─────────────────────────────────────────────
# Cross-Institutional Monitor
# ─────────────────────────────────────────────

def evaluate_continuity_object(obj: ContinuityObject) -> dict:
    """
    Evaluate all active domains for a continuity object.
    Returns a unified picture: per-domain states, worst state,
    cascading failures, and a combined admissibility verdict.
    """
    snapshot_id = str(uuid.uuid4())
    timestamp   = datetime.now(timezone.utc).isoformat()
    results     = {}
    states      = {}

    for domain, state in obj.domains.items():
        result = evaluate({
            "domain":    domain,
            "label":     f"{obj.label} — {domain}",
            "case_id":   f"{obj.subject_id}::{domain}",
            "state":     state,
        })
        results[domain] = result
        states[domain]  = result["boundary_state"]

    # Rank states worst-first
    rank = {
        BoundaryState.NON_EXECUTABLE.value: 0,
        BoundaryState.NON_ADMISSIBLE.value: 1,
        BoundaryState.DEGRADED.value:       2,
        BoundaryState.CONTINUE.value:       3,
    }
    sorted_domains = sorted(states.items(), key=lambda kv: rank.get(kv[1], 9))
    worst_state    = sorted_domains[0][1] if sorted_domains else BoundaryState.CONTINUE.value

    # Detect cascading: domains that are NON-ADMISSIBLE/NON-EXECUTABLE
    # AND have dependencies on other active domains
    non_admissible_domains = [
        d for d, s in states.items()
        if s in (BoundaryState.NON_ADMISSIBLE.value, BoundaryState.NON_EXECUTABLE.value)
    ]
    cascading_risk = []
    for d in non_admissible_domains:
        dependents = CROSS_DOMAIN_TRIGGERS.get(d, [])
        active_dependents = [dep for dep in dependents if dep in states]
        if active_dependents:
            cascading_risk.append({
                "failing_domain": d,
                "at_risk_domains": active_dependents,
            })

    # Compound non-admissibility: situations where NO single domain
    # triggers an alert but the combined picture is non-admissible
    degraded_domains = [d for d, s in states.items() if s == BoundaryState.DEGRADED.value]
    compound_non_admissible = (
        worst_state == BoundaryState.DEGRADED.value
        and len(degraded_domains) >= 3
    )

    snapshot = {
        "snapshot_id":             snapshot_id,
        "subject_id":              obj.subject_id,
        "label":                   obj.label,
        "timestamp":               timestamp,
        "combined_state":          worst_state,
        "compound_non_admissible": compound_non_admissible,
        "domain_states":           states,
        "domain_results":          results,
        "non_admissible_domains":  non_admissible_domains,
        "degraded_domains":        degraded_domains,
        "cascading_risk":          cascading_risk,
        "domains_evaluated":       len(results),
        "alert": (
            worst_state in (BoundaryState.NON_ADMISSIBLE.value, BoundaryState.NON_EXECUTABLE.value)
            or compound_non_admissible
        ),
    }

    obj.history.append(snapshot)
    return snapshot


def evaluate_population(objects: list[ContinuityObject]) -> dict:
    """
    Evaluate a cohort of continuity objects simultaneously.
    Returns population-level state, aggregate counts, and flagged subjects.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    results   = [evaluate_continuity_object(obj) for obj in objects]

    state_counts = {
        BoundaryState.CONTINUE.value:       0,
        BoundaryState.DEGRADED.value:       0,
        BoundaryState.NON_ADMISSIBLE.value: 0,
        BoundaryState.NON_EXECUTABLE.value: 0,
    }
    for r in results:
        s = r["combined_state"]
        state_counts[s] = state_counts.get(s, 0) + 1

    flagged = [r for r in results if r["alert"]]
    non_executable = [r for r in results if r["combined_state"] == BoundaryState.NON_EXECUTABLE.value]

    return {
        "population_snapshot_id": str(uuid.uuid4()),
        "timestamp":              timestamp,
        "total_subjects":         len(results),
        "state_counts":           state_counts,
        "flagged_count":          len(flagged),
        "non_executable_count":   len(non_executable),
        "flagged_subjects":       flagged,
        "all_results":            results,
    }
