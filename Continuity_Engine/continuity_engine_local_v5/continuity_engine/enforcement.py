from __future__ import annotations

from typing import List
from .models import CaseInput, IAFResult, AdmissibilityClass


def generate_actions(case: CaseInput, admissibility: AdmissibilityClass, iaf: IAFResult, broken: List[str]) -> List[str]:
    actions: List[str] = []

    if admissibility == "admissible":
        actions.append("Continue only on currently valid trajectories and preserve timing reserve")
    if admissibility in {"degraded", "restricted"}:
        actions.append("Restrict execution to explicitly valid paths only")
        actions.append("Require accountable operator confirmation before each continuation step")
    if admissibility == "containment-required":
        actions.append("Contain propagation immediately and suspend non-essential execution")
        actions.append("Invalidate dependent outputs until bounded verification is restored")
    if admissibility in {"halt-required", "non-executable", "uncertifiable"}:
        actions.append("Stop continuation immediately")
        actions.append("Block downstream execution and mark current state non-admissible")
        actions.append("Prevent workflow completion, actuation, or closure until restoration criteria are met")

    if iaf.offline_mode_engaged:
        actions.append("Engage offline-first local mode and disable remote-only features")
    if not iaf.network_dependent_execution_admissible:
        actions.append("Disable remote sync, internet-dependent workflows, and external network execution")
    if not iaf.local_execution_admissible:
        actions.append("Local execution path is not admissible under current connectivity/certificate state")
    if iaf.broken_certificates:
        actions.append("Treat certificate-dependent execution as blocked until valid or fallback credentials exist")
    if not iaf.restoration_reachable:
        actions.append("No valid recovery trajectory exists; do not resume until a new bounded path is created")
    if not iaf.truth_integrity_ok:
        actions.append("Freeze decisions based on stale, conflicting, or unverifiable truth")
    if not iaf.authority_reachable:
        actions.append("Escalation is formally defined but not reachable; treat as absence of authority")
    if broken:
        actions.append("Resolve broken dependencies: " + "; ".join(broken[:6]))
    if not case.future_state_preserved:
        actions.append("Redesign current path to preserve at least one admissible future trajectory")
    if case.pressure > 0.7:
        actions.append("Reduce load, backlog, or surge pressure before any re-entry")
    if case.resonance > 0.7:
        actions.append("Decouple interacting pathways to reduce resonance amplification")

    blocked_paths = [p.name for p in iaf.path_evaluations if not p.valid]
    viable_paths = [p.name for p in iaf.path_evaluations if p.valid]
    if blocked_paths:
        actions.append("Blocked recovery trajectories: " + "; ".join(blocked_paths[:6]))
    if viable_paths:
        actions.append("Only these recovery trajectories remain admissible: " + "; ".join(viable_paths[:6]))

    if iaf.propagated_failures:
        actions.append("Trigger immediate re-evaluation in dependent systems: " + "; ".join(iaf.propagated_failures[:6]))

    actions.append(f"Point of no return status: last admissible action = {iaf.last_admissible_action}")
    actions.append(f"Connectivity state: {iaf.connection_reason}")
    actions.append(f"Certificate state: {iaf.certificate_reason}")

    deduped: List[str] = []
    for action in actions:
        if action not in deduped:
            deduped.append(action)
    return deduped or ["No action generated"]
