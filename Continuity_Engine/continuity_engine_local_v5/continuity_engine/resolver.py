from __future__ import annotations

from datetime import datetime, timezone
from .models import CaseInput, EvaluationResult
from .iaf import solve_iaf
from .topology import broken_dependencies
from .enforcement import generate_actions


def evaluate_case(case: CaseInput) -> EvaluationResult:
    iaf = solve_iaf(case)
    broken = broken_dependencies(case)
    total_interval = sum(interval.current_minutes for interval in case.intervals)
    timing_margin = case.time_to_irreversibility_minutes - total_interval

    if not iaf.truth_integrity_ok:
        admissibility = "uncertifiable"
    elif not iaf.restoration_reachable or not iaf.interval_continuity or not iaf.trajectory_valid:
        admissibility = "non-executable"
    elif not iaf.propagation_bounded:
        admissibility = "containment-required"
    elif not iaf.dependency_integrity or not iaf.authority_reachable:
        admissibility = "restricted"
    elif iaf.irreversibility_budget < 0.15:
        admissibility = "halt-required"
    elif iaf.irreversibility_budget < 0.35:
        admissibility = "degraded"
    else:
        admissibility = "admissible"

    actions = generate_actions(case, admissibility, iaf, broken)

    return EvaluationResult(
        case_title=case.title,
        domain=case.domain,
        admissibility_class=admissibility,
        reasons=iaf.reasoning,
        required_actions=actions,
        recovery_reachable=iaf.restoration_reachable,
        timing_margin_minutes=timing_margin,
        broken_dependencies=broken,
        report_timestamp=datetime.now(timezone.utc).isoformat(),
        iaf=iaf,
    )
