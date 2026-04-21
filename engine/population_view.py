"""
Boundary — Population-Level Continuity View

Evaluates not one case but a cohort simultaneously.
Aggregate state, timing margins, and cascading dependencies
are visible at once.

This is the collective gap: continuity failures often happen in clusters
— a care home, a ward, a refugee settlement, a disaster zone — where
many people are simultaneously in non-admissible states.

This module makes the cluster visible.
"""

import uuid
from datetime import datetime, timezone
from collections import defaultdict
from engine.continuity_monitor import ContinuityObject, evaluate_continuity_object
from engine.boundary_engine import BoundaryState


# ─────────────────────────────────────────────
# Cohort
# ─────────────────────────────────────────────

class Cohort:
    """
    A named group of continuity objects — a ward, care home,
    settlement, team, or any defined population.
    """

    def __init__(self, cohort_id: str, label: str, context: str = ""):
        self.cohort_id   = cohort_id
        self.label       = label
        self.context     = context  # e.g. "NHS Ward 7B", "Refugee Settlement Alpha"
        self.subjects:   dict[str, ContinuityObject] = {}
        self.snapshots:  list[dict] = []
        self.created_at  = datetime.now(timezone.utc).isoformat()

    def add_subject(self, subject: ContinuityObject):
        self.subjects[subject.subject_id] = subject

    def remove_subject(self, subject_id: str):
        self.subjects.pop(subject_id, None)

    def update_subject_domain(self, subject_id: str, domain: str, state: dict):
        if subject_id not in self.subjects:
            self.subjects[subject_id] = ContinuityObject(subject_id)
        self.subjects[subject_id].set_domain_state(domain, state)


# ─────────────────────────────────────────────
# Population Evaluator
# ─────────────────────────────────────────────

def evaluate_cohort(cohort: Cohort) -> dict:
    """
    Evaluate all subjects in a cohort simultaneously.
    Returns a population snapshot with:
      - Per-subject combined state
      - Aggregate counts and rates
      - Subjects requiring immediate action
      - Domain-level clustering (multiple subjects failing same domain)
      - Cascading risk across the cohort
    """
    snapshot_id = str(uuid.uuid4())
    timestamp   = datetime.now(timezone.utc).isoformat()

    subject_results = []
    for subj in cohort.subjects.values():
        result = evaluate_continuity_object(subj)
        subject_results.append(result)

    # Aggregate state counts
    state_counts = defaultdict(int)
    for r in subject_results:
        state_counts[r["combined_state"]] += 1

    non_executable  = [r for r in subject_results if r["combined_state"] == BoundaryState.NON_EXECUTABLE.value]
    non_admissible  = [r for r in subject_results if r["combined_state"] == BoundaryState.NON_ADMISSIBLE.value]
    degraded        = [r for r in subject_results if r["combined_state"] == BoundaryState.DEGRADED.value]
    flagged         = [r for r in subject_results if r["alert"]]

    # Domain clustering: which domains are failing across multiple subjects?
    domain_failure_counts: dict[str, int] = defaultdict(int)
    domain_non_executable:  dict[str, int] = defaultdict(int)
    for r in subject_results:
        for d in r.get("non_admissible_domains", []):
            domain_failure_counts[d] += 1
        for d in r.get("non_admissible_domains", []):
            if r["combined_state"] == BoundaryState.NON_EXECUTABLE.value:
                domain_non_executable[d] += 1

    # Clustered domains: 3+ subjects failing the same domain = systemic signal
    clustered_domains = {
        d: count for d, count in domain_failure_counts.items()
        if count >= 3
    }

    # Cascade chains: subjects whose failure could propagate to others
    cascade_risk_subjects = [
        r for r in subject_results if r.get("cascading_risk")
    ]

    # Overall population state: worst individual state
    rank = {
        BoundaryState.NON_EXECUTABLE.value: 0,
        BoundaryState.NON_ADMISSIBLE.value: 1,
        BoundaryState.DEGRADED.value:       2,
        BoundaryState.CONTINUE.value:       3,
    }
    if subject_results:
        population_state = min(
            [r["combined_state"] for r in subject_results],
            key=lambda s: rank.get(s, 9)
        )
    else:
        population_state = BoundaryState.CONTINUE.value

    # Alert: any non-admissible, OR 30%+ degraded, OR clustered domain failure
    degraded_rate = len(degraded) / max(len(subject_results), 1)
    population_alert = (
        len(non_executable) > 0
        or len(non_admissible) > 0
        or degraded_rate >= 0.3
        or len(clustered_domains) > 0
    )

    snapshot = {
        "snapshot_id":           snapshot_id,
        "cohort_id":             cohort.cohort_id,
        "label":                 cohort.label,
        "context":               cohort.context,
        "timestamp":             timestamp,
        "total_subjects":        len(subject_results),
        "population_state":      population_state,
        "population_alert":      population_alert,

        # Counts
        "non_executable_count":  len(non_executable),
        "non_admissible_count":  len(non_admissible),
        "degraded_count":        len(degraded),
        "continue_count":        state_counts.get(BoundaryState.CONTINUE.value, 0),
        "flagged_count":         len(flagged),
        "degraded_rate":         round(degraded_rate, 3),

        # Domain analysis
        "domain_failure_counts": dict(domain_failure_counts),
        "clustered_domains":     clustered_domains,
        "cascade_risk_count":    len(cascade_risk_subjects),

        # Detail
        "non_executable_subjects": non_executable,
        "non_admissible_subjects": non_admissible,
        "flagged_subjects":        flagged,
        "all_subject_results":     subject_results,
    }

    cohort.snapshots.append(snapshot)
    return snapshot


def compare_cohort_snapshots(cohort: Cohort) -> dict:
    """
    Compare the last two snapshots of a cohort to detect
    worsening, improving, or stable trends.
    """
    if len(cohort.snapshots) < 2:
        return {"comparison": "insufficient_snapshots"}

    prev = cohort.snapshots[-2]
    curr = cohort.snapshots[-1]

    def _delta(key):
        return curr.get(key, 0) - prev.get(key, 0)

    return {
        "comparison_type": "snapshot_delta",
        "from_timestamp":  prev["timestamp"],
        "to_timestamp":    curr["timestamp"],
        "deltas": {
            "non_executable":  _delta("non_executable_count"),
            "non_admissible":  _delta("non_admissible_count"),
            "degraded":        _delta("degraded_count"),
            "continue":        _delta("continue_count"),
        },
        "trend": (
            "WORSENING" if _delta("non_executable_count") > 0 or _delta("non_admissible_count") > 0
            else "IMPROVING" if _delta("non_executable_count") < 0 and _delta("degraded_count") <= 0
            else "STABLE"
        ),
        "new_clustered_domains": {
            d: c for d, c in curr.get("clustered_domains", {}).items()
            if d not in prev.get("clustered_domains", {})
        },
    }


# ─────────────────────────────────────────────
# Quick cohort builder from flat data
# ─────────────────────────────────────────────

def build_cohort_from_list(
    cohort_id: str,
    label: str,
    subjects: list[dict],
) -> Cohort:
    """
    Build a cohort from a flat list of subject dicts.

    Each subject dict:
      { "subject_id": "...", "label": "...", "domains": {"pharmacological": {...}, ...} }
    """
    cohort = Cohort(cohort_id, label)
    for s in subjects:
        obj = ContinuityObject(s["subject_id"], s.get("label", ""))
        for domain, state in s.get("domains", {}).items():
            obj.set_domain_state(domain, state)
        cohort.add_subject(obj)
    return cohort
