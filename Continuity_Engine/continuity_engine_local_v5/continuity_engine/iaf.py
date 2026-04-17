from __future__ import annotations

from .models import CaseInput, IAFResult, PathEvaluation
from .topology import broken_dependencies, path_blockers

ORDERED_INTERVALS = [
    "detection",
    "interpretation",
    "decision",
    "response",
    "enforcement",
    "restoration",
    "verification",
]


def _point_of_no_return(case: CaseInput) -> tuple[float, str]:
    remaining = case.time_to_irreversibility_minutes
    cumulative = 0.0
    label = "start"
    interval_map = {interval.name: interval for interval in case.intervals}
    for name in ORDERED_INTERVALS:
        interval = interval_map.get(name)
        if not interval:
            continue
        cumulative += interval.current_minutes
        if cumulative <= remaining:
            label = name
        else:
            return max(0.0, remaining - cumulative), label
    return max(0.0, remaining - cumulative), label


def _truth_integrity(case: CaseInput) -> tuple[bool, list[str]]:
    issues: list[str] = []
    for signal in case.signal_sources:
        if not signal.verifiable:
            issues.append(f"Signal unverifiable: {signal.name}")
        if signal.stale or signal.observed_minutes_ago > signal.max_age_minutes:
            issues.append(f"Signal stale: {signal.name}")
        if signal.conflicted:
            issues.append(f"Signal conflicted: {signal.name}")
    if not case.signal_sources:
        unverifiable_entities = [e.name for e in case.entities if not e.verifiable]
        issues.extend([f"Entity unverifiable: {name}" for name in unverifiable_entities])
    return len(issues) == 0, issues


def _authority_reality(case: CaseInput) -> tuple[bool, str]:
    authority_entities = [e for e in case.entities if e.type in {"team", "institution", "interface"}]
    if not authority_entities:
        return False, "No reachable authority entity defined"
    reachable = [e for e in authority_entities if e.reachable and e.availability >= 0.5]
    if reachable:
        names = ", ".join(e.name for e in reachable[:3])
        return True, f"Reachable authority entities available: {names}"
    return False, "Escalation defined but no reachable authority entity can act in time"


def _connectivity_and_certificates(case: CaseInput) -> tuple[bool, bool, bool, str, str, int, int]:
    profile = case.connectivity
    offline_mode_engaged = profile.mode in {"offline", "degraded"} or not profile.remote_sync_enabled

    local_execution_admissible = True
    network_execution_admissible = True
    connection_reason = "Local execution path available"
    certificate_reason = "No certificate dependency blocking current path"

    if profile.network_required_for_local_use and profile.mode != "online":
        local_execution_admissible = False
        connection_reason = "Local execution depends on network, but connection is not online"
    elif profile.network_required_for_primary_path and profile.mode != "online":
        if profile.fallback_local_mode_available:
            network_execution_admissible = False
            connection_reason = "Primary network path unavailable; fallback local mode engaged"
        else:
            local_execution_admissible = False
            network_execution_admissible = False
            connection_reason = "Primary network path unavailable and no fallback local mode exists"
    elif profile.mode == "degraded":
        network_execution_admissible = False
        connection_reason = "Network degraded; remote path not admissible, local fallback permitted"
    elif profile.mode == "offline":
        network_execution_admissible = False
        connection_reason = "Offline mode active; remote path not admissible, local fallback permitted"

    valid_certificates = 0
    broken_certificates = 0
    broken_messages: list[str] = []
    for cert in profile.certificate_dependencies:
        if cert.status == "valid":
            valid_certificates += 1
            continue
        if cert.continuity_critical:
            broken_certificates += 1
            broken_messages.append(f"{cert.name} ({cert.required_for}: {cert.status})")
            if cert.required_for == "local_execution":
                local_execution_admissible = local_execution_admissible and cert.fallback_exists
            else:
                network_execution_admissible = network_execution_admissible and cert.fallback_exists

    if broken_messages:
        certificate_reason = "Broken certificate dependencies: " + "; ".join(broken_messages[:6])
    elif profile.certificate_dependencies:
        certificate_reason = "All required certificates for the evaluated path are valid"

    return (
        offline_mode_engaged,
        local_execution_admissible,
        network_execution_admissible,
        connection_reason,
        certificate_reason,
        valid_certificates,
        broken_certificates,
    )


def _propagate_failures(case: CaseInput, broken: list[str], candidate_class: str) -> list[str]:
    propagated: list[str] = []
    if candidate_class in {"non-executable", "containment-required", "uncertifiable", "halt-required"}:
        for downstream in case.downstream_systems:
            if downstream.dependency_on_case >= 0.4:
                consequence = "invalidated" if downstream.irreversible_if_invalid else "requires immediate re-evaluation"
                propagated.append(f"{downstream.name} {consequence}")
    if broken and not propagated:
        for dependency in broken[:3]:
            propagated.append(f"Dependent path affected by {dependency}")
    return propagated


def solve_iaf(case: CaseInput) -> IAFResult:
    reasons: list[str] = []
    proof_lines: list[str] = []
    broken = broken_dependencies(case)
    dependency_integrity = len(broken) == 0
    if broken:
        reasons.extend(broken)

    total_interval = sum(interval.current_minutes for interval in case.intervals)
    timing_margin = case.time_to_irreversibility_minutes - total_interval
    interval_continuity = timing_margin >= 0
    if not interval_continuity:
        reasons.append(
            f"Total active interval {total_interval:.1f}m exceeds time-to-irreversibility {case.time_to_irreversibility_minutes:.1f}m"
        )

    max_interval_violations = [
        f"{interval.name} exceeds bound ({interval.current_minutes:.1f}m > {interval.max_minutes:.1f}m)"
        for interval in case.intervals
        if interval.current_minutes > interval.max_minutes
    ]
    if max_interval_violations:
        interval_continuity = False
        reasons.extend(max_interval_violations)

    point_of_no_return_minutes, last_admissible_action = _point_of_no_return(case)

    path_evaluations: list[PathEvaluation] = []
    for path in case.recovery_paths:
        blockers = path_blockers(case, path)
        path_margin = case.time_to_irreversibility_minutes - (total_interval + path.bounded_minutes)
        within_time = path_margin >= 0
        valid = path.executable and within_time and not blockers and (interval_continuity or path.degraded_mode_valid)
        if not path.executable:
            blockers.append("Path marked non-executable")
        if not within_time:
            blockers.append(
                f"Path exceeds remaining window ({total_interval + path.bounded_minutes:.1f}m > {case.time_to_irreversibility_minutes:.1f}m)"
            )
        if not interval_continuity and not path.degraded_mode_valid:
            blockers.append("Base execution interval already non-admissible")
        pnr = case.time_to_irreversibility_minutes - (total_interval + max(0.0, path.bounded_minutes))
        path_evaluations.append(
            PathEvaluation(
                name=path.name,
                valid=valid,
                bounded_minutes=path.bounded_minutes,
                margin_minutes=path_margin,
                degraded_mode_valid=path.degraded_mode_valid,
                blockers=blockers,
                last_admissible_action_minutes=max(0.0, path_margin),
                point_of_no_return_minutes=pnr,
            )
        )

    viable_paths = [path for path in path_evaluations if path.valid]
    restoration_reachable = bool(viable_paths)

    truth_integrity_ok, truth_issues = _truth_integrity(case)
    if not truth_integrity_ok:
        reasons.extend(truth_issues)

    authority_reachable, authority_reason = _authority_reality(case)
    if not authority_reachable:
        reasons.append(authority_reason)

    (
        offline_mode_engaged,
        local_execution_admissible,
        network_execution_admissible,
        connection_reason,
        certificate_reason,
        valid_certificates,
        broken_certificates,
    ) = _connectivity_and_certificates(case)
    if not local_execution_admissible:
        reasons.append(connection_reason)
    if broken_certificates:
        reasons.append(certificate_reason)

    propagation_load = case.pressure + case.resonance + (0.25 if broken else 0.0) + (0.2 if not truth_integrity_ok else 0.0)
    propagation_bounded = propagation_load < 1.0
    if not propagation_bounded:
        reasons.append(f"Pressure/resonance exceed control envelope ({propagation_load:.2f} >= 1.00)")

    trajectory_valid = (
        restoration_reachable
        and interval_continuity
        and dependency_integrity
        and case.future_state_preserved
        and truth_integrity_ok
        and authority_reachable
        and propagation_bounded
        and local_execution_admissible
    )

    if not restoration_reachable:
        reasons.append("No recovery path remains reachable within the recoverability window")
    if not case.future_state_preserved:
        reasons.append("Future admissible state space is not preserved")
    if not network_execution_admissible and local_execution_admissible:
        reasons.append("Network-dependent execution is non-admissible; local fallback remains available")

    budget = max(0.0, min(1.0, timing_margin / case.time_to_irreversibility_minutes))
    budget = max(
        0.0,
        min(
            1.0,
            budget
            - (case.pressure * 0.25)
            - (case.resonance * 0.25)
            - (0.15 if broken else 0.0)
            - (0.15 if not truth_integrity_ok else 0.0)
            - (0.10 if not network_execution_admissible else 0.0),
        ),
    )

    candidate_class = "admissible" if trajectory_valid else "non-executable"
    if trajectory_valid and budget < 0.15:
        candidate_class = "halt-required"
    elif trajectory_valid and not dependency_integrity:
        candidate_class = "restricted"
    elif trajectory_valid and budget < 0.35:
        candidate_class = "degraded"
    elif not propagation_bounded:
        candidate_class = "containment-required"

    propagated_failures = _propagate_failures(case, broken, candidate_class)
    if propagated_failures:
        reasons.extend([f"Propagation: {line}" for line in propagated_failures])

    proof_lines.append(f"Total active interval = {total_interval:.1f}m; time-to-irreversibility = {case.time_to_irreversibility_minutes:.1f}m")
    proof_lines.append(f"Valid recovery trajectories = {len(viable_paths)} / {len(path_evaluations)}")
    proof_lines.append(f"Dependency integrity = {dependency_integrity}")
    proof_lines.append(f"Truth integrity = {truth_integrity_ok}")
    proof_lines.append(f"Authority reachable = {authority_reachable}")
    proof_lines.append(f"Propagation bounded = {propagation_bounded}")
    proof_lines.append(f"Future admissible state preserved = {case.future_state_preserved}")
    proof_lines.append(f"Offline mode engaged = {offline_mode_engaged}")
    proof_lines.append(f"Local execution admissible = {local_execution_admissible}")
    proof_lines.append(f"Network-dependent execution admissible = {network_execution_admissible}")
    proof_lines.append(f"Certificate status = {valid_certificates} valid / {broken_certificates} broken")
    if trajectory_valid:
        proof_lines.append("At least one fully bounded, reachable, verifiable, and locally executable trajectory exists.")
    else:
        proof_lines.append("No fully bounded, reachable, verifiable, and locally executable continuation trajectory exists.")

    return IAFResult(
        restoration_reachable=restoration_reachable,
        propagation_bounded=propagation_bounded,
        interval_continuity=interval_continuity,
        dependency_integrity=dependency_integrity,
        future_state_preserved=case.future_state_preserved,
        trajectory_valid=trajectory_valid,
        viable_recovery_path_count=len(viable_paths),
        blocked_recovery_path_count=len(path_evaluations) - len(viable_paths),
        path_evaluations=path_evaluations,
        irreversibility_budget=budget,
        point_of_no_return_minutes=point_of_no_return_minutes,
        last_admissible_action=last_admissible_action,
        proof_lines=proof_lines,
        truth_integrity_ok=truth_integrity_ok,
        authority_reachable=authority_reachable,
        authority_reason=authority_reason,
        propagated_failures=propagated_failures,
        reasoning=reasons,
        offline_mode_engaged=offline_mode_engaged,
        local_execution_admissible=local_execution_admissible,
        network_dependent_execution_admissible=network_execution_admissible,
        connection_reason=connection_reason,
        certificate_reason=certificate_reason,
        valid_certificates=valid_certificates,
        broken_certificates=broken_certificates,
    )
