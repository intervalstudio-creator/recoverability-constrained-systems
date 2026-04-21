"""
Boundary Engine v4.0
Recoverability-Constrained Execution Platform

Core Principle:
  A system may only execute where recoverability can be established in time
  under real conditions as sufficient to prevent irreversible transition.
  If recoverability cannot be established, execution does not occur.

Output states ONLY:
  CONTINUE        - all recoverability conditions met, execution admissible
  DEGRADED        - one or more conditions weakened, margin reduced, monitor closely
  NON-ADMISSIBLE  - recoverability cannot be established, execution must not proceed
  NON-EXECUTABLE  - non-admissible + time window collapsed or human authority unreachable;
                    escalation is required, continuation must not occur

Execution is admissible only if ALL SIX conditions hold:
  1. Recovery path exists
  2. Recovery path is reachable
  3. Failure can be detected in time
  4. Response can occur in time
  5. Recovery can be executed in time
  6. No irreversible transition occurs before recovery

If any condition fails: NON-ADMISSIBLE.
If time window has collapsed or authority is unreachable: NON-EXECUTABLE.

Unknown = NON-ADMISSIBLE (not DEGRADED — unknown is not a weakened state,
it is an unestablished one, and unestablished recoverability is non-admissible).

This engine makes NO clinical, legal, financial, or operational decisions.
It evaluates recoverability and requires visibility and escalation only.
"""

import json
import time
import uuid
import logging
from datetime import datetime, timezone
from typing import Any
from enum import Enum

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("boundary_engine")


# ─────────────────────────────────────────────
# Output States
# ─────────────────────────────────────────────

class BoundaryState(str, Enum):
    CONTINUE       = "CONTINUE"
    DEGRADED       = "DEGRADED"
    NON_ADMISSIBLE = "NON-ADMISSIBLE"
    NON_EXECUTABLE = "NON-EXECUTABLE"


# ─────────────────────────────────────────────
# Domain Registry
# ─────────────────────────────────────────────

SUPPORTED_DOMAINS = [
    "pharmacological",
    "healthcare",
    "identity",
    "finance",
    "housing",
    "legal",
    "labour",
    "education",
    "infrastructure",
    "disaster",
    "transport",
    "supply_chain",
    "energy",
    "communications",
    "food_water",
]


# ─────────────────────────────────────────────
# Invariant Layer (global, always evaluated first)
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# The Six Recoverability Conditions (Global — always evaluated first)
# These are the foundational conditions from the Execution Constraint layer.
# All six must hold for execution to be admissible.
# ─────────────────────────────────────────────

GLOBAL_INVARIANTS = [
    {
        "id": "RC-001",
        "name": "recovery_path_exists",
        "description": "A recovery path must exist. (Condition 1: recovery path exists)",
        "field": "recovery_path_exists",
        "required_value": True,
        "weight": "critical",
    },
    {
        "id": "RC-002",
        "name": "recovery_path_reachable",
        "description": "The recovery path must be reachable under real conditions. (Condition 2: recovery path is reachable)",
        "field": "recovery_path_reachable",
        "required_value": True,
        "weight": "critical",
    },
    {
        "id": "RC-003",
        "name": "failure_detectable_in_time",
        "description": "Failure must be detectable before the irreversibility threshold. (Condition 3: failure can be detected in time)",
        "field": "failure_detectable_in_time",
        "required_value": True,
        "weight": "critical",
    },
    {
        "id": "RC-004",
        "name": "response_possible_in_time",
        "description": "A response must be possible within the available time window. (Condition 4: response can occur in time)",
        "field": "response_possible_in_time",
        "required_value": True,
        "weight": "critical",
    },
    {
        "id": "RC-005",
        "name": "recovery_executable_in_time",
        "description": "Recovery must be fully executable before irreversible transition. (Condition 5: recovery can be executed in time)",
        "field": "recovery_executable_in_time",
        "required_value": True,
        "weight": "critical",
    },
    {
        "id": "RC-006",
        "name": "no_irreversible_transition_before_recovery",
        "description": "No irreversible transition must occur before recovery completes. (Condition 6: no irreversible transition before recovery)",
        "field": "no_irreversible_transition_before_recovery",
        "required_value": True,
        "weight": "critical",
    },
    # ── Execution gate conditions ──
    {
        "id": "GI-001",
        "name": "human_authority_reachable",
        "description": "A responsible human authority must be reachable within the timing window.",
        "field": "human_authority_reachable",
        "required_value": True,
        "weight": "execution_gate",  # NON-EXECUTABLE if this fails with NON-ADMISSIBLE
    },
    {
        "id": "GI-002",
        "name": "timing_window_open",
        "description": "Time remaining before irreversibility must be positive.",
        "field": "time_remaining_seconds",
        "required_min": 1,
        "weight": "execution_gate",
    },
    {
        "id": "GI-003",
        "name": "override_attributed",
        "description": "Any active override must have logged identity and reason.",
        "field": "override_attributed",
        "required_value": True,
        "conditional_on": "override_active",
        "weight": "critical",
    },
    {
        "id": "GI-004",
        "name": "fallback_path_available",
        "description": "At least one fallback path must be identified.",
        "field": "fallback_path_available",
        "required_value": True,
        "weight": "major",
    },
]


# ─────────────────────────────────────────────
# Domain Rule Packs
# ─────────────────────────────────────────────

DOMAIN_RULES = {
    "pharmacological": [
        {"id": "PH-001", "name": "supply_available", "field": "supply_days_remaining", "required_min": 1, "weight": "critical", "description": "Medication supply must be available."},
        {"id": "PH-002", "name": "prescriber_reachable", "field": "prescriber_reachable", "required_value": True, "weight": "critical", "description": "Prescribing authority must be reachable."},
        {"id": "PH-003", "name": "no_abrupt_discontinuation_risk", "field": "abrupt_stop_risk", "required_value": False, "weight": "critical", "description": "Abrupt discontinuation must not pose irreversible risk."},
        {"id": "PH-004", "name": "dispensing_accessible", "field": "dispensing_accessible", "required_value": True, "weight": "major", "description": "Dispensing point must be physically/logistically accessible."},
        {"id": "PH-005", "name": "taper_plan_exists_if_needed", "field": "taper_plan_exists", "required_value": True, "conditional_on": "taper_required", "weight": "critical", "description": "If tapering is required, a taper plan must exist."},
        {"id": "PH-006", "name": "polypharmacy_interaction_cleared", "field": "interaction_flag", "required_value": False, "weight": "major", "description": "No unresolved dangerous interactions flagged."},
    ],
    "healthcare": [
        {"id": "HC-001", "name": "appointment_not_missed_critically", "field": "critical_appointment_missed", "required_value": False, "weight": "critical"},
        {"id": "HC-002", "name": "diagnostics_not_delayed_beyond_window", "field": "diagnostic_delay_days", "required_max": 7, "weight": "major"},
        {"id": "HC-003", "name": "transport_to_care_available", "field": "transport_available", "required_value": True, "weight": "major"},
        {"id": "HC-004", "name": "caregiver_not_collapsed", "field": "caregiver_available", "required_value": True, "weight": "critical"},
        {"id": "HC-005", "name": "oxygen_supply_intact", "field": "oxygen_interrupted", "required_value": False, "conditional_on": "oxygen_dependent", "weight": "critical"},
        {"id": "HC-006", "name": "discharge_safe", "field": "discharge_safe", "required_value": True, "conditional_on": "pending_discharge", "weight": "critical"},
    ],
    "identity": [
        {"id": "ID-001", "name": "identity_document_available", "field": "id_document_available", "required_value": True, "weight": "major"},
        {"id": "ID-002", "name": "access_recovery_path_exists", "field": "access_recovery_available", "required_value": True, "weight": "major"},
        {"id": "ID-003", "name": "payroll_identity_intact", "field": "payroll_identity_intact", "required_value": True, "weight": "major"},
        {"id": "ID-004", "name": "no_cross_institution_gap", "field": "institution_portability_gap", "required_value": False, "weight": "minor"},
    ],
    "finance": [
        {"id": "FI-001", "name": "bank_access_not_locked", "field": "bank_locked", "required_value": False, "weight": "critical"},
        {"id": "FI-002", "name": "essential_payment_not_interrupted", "field": "essential_payment_blocked", "required_value": False, "weight": "critical"},
        {"id": "FI-003", "name": "income_not_interrupted", "field": "income_interrupted", "required_value": False, "weight": "major"},
        {"id": "FI-004", "name": "no_single_provider_dependency_at_risk", "field": "single_provider_risk", "required_value": False, "weight": "minor"},
    ],
    "housing": [
        {"id": "HO-001", "name": "no_imminent_eviction", "field": "eviction_imminent", "required_value": False, "weight": "critical"},
        {"id": "HO-002", "name": "utilities_not_disconnected", "field": "utilities_disconnected", "required_value": False, "weight": "major"},
        {"id": "HO-003", "name": "shelter_habitable", "field": "habitability_failure", "required_value": False, "weight": "critical"},
        {"id": "HO-004", "name": "re_entry_possible", "field": "re_entry_blocked", "required_value": False, "weight": "major"},
    ],
    "legal": [
        {"id": "LE-001", "name": "remedy_reachable", "field": "remedy_unreachable", "required_value": False, "weight": "critical"},
        {"id": "LE-002", "name": "court_timing_not_missed", "field": "court_deadline_missed", "required_value": False, "weight": "critical"},
        {"id": "LE-003", "name": "enforcement_not_gapped", "field": "enforcement_gap", "required_value": False, "weight": "major"},
    ],
    "labour": [
        {"id": "LA-001", "name": "wage_not_interrupted", "field": "wage_interrupted", "required_value": False, "weight": "major"},
        {"id": "LA-002", "name": "rest_interval_not_violated", "field": "rest_violation", "required_value": False, "weight": "major"},
        {"id": "LA-003", "name": "unsafe_shift_not_scheduled", "field": "unsafe_shift", "required_value": False, "weight": "major"},
    ],
    "infrastructure": [
        {"id": "IN-001", "name": "power_not_failed", "field": "power_failure", "required_value": False, "weight": "critical"},
        {"id": "IN-002", "name": "network_not_failed", "field": "network_failure", "required_value": False, "weight": "major"},
        {"id": "IN-003", "name": "control_not_lost", "field": "control_loss", "required_value": False, "weight": "critical"},
        {"id": "IN-004", "name": "degraded_mode_defined", "field": "degraded_mode_available", "required_value": True, "weight": "major"},
    ],
    "disaster": [
        {"id": "DI-001", "name": "evacuation_window_open", "field": "evacuation_window_closed", "required_value": False, "weight": "critical"},
        {"id": "DI-002", "name": "shelter_assigned", "field": "shelter_assigned", "required_value": True, "weight": "critical"},
        {"id": "DI-003", "name": "communications_not_collapsed", "field": "comms_collapsed", "required_value": False, "weight": "major"},
    ],
    "transport": [
        {"id": "TR-001", "name": "route_available", "field": "route_blocked", "required_value": False, "weight": "major"},
        {"id": "TR-002", "name": "timing_not_missed", "field": "timing_missed", "required_value": False, "weight": "major"},
    ],
    "education": [
        {"id": "ED-001", "name": "learning_access_not_excluded", "field": "learning_excluded", "required_value": False, "weight": "major"},
        {"id": "ED-002", "name": "progression_not_interrupted", "field": "progression_interrupted", "required_value": False, "weight": "minor"},
    ],
    "energy": [
        {"id": "EN-001", "name": "energy_supply_not_interrupted", "field": "energy_interrupted", "required_value": False, "weight": "critical"},
        {"id": "EN-002", "name": "backup_source_available", "field": "backup_energy_available", "required_value": True, "weight": "major"},
    ],
    "communications": [
        {"id": "CO-001", "name": "primary_comms_available", "field": "primary_comms_down", "required_value": False, "weight": "major"},
        {"id": "CO-002", "name": "fallback_comms_available", "field": "fallback_comms_available", "required_value": True, "weight": "major"},
    ],
    "food_water": [
        {"id": "FW-001", "name": "food_access_not_interrupted", "field": "food_interrupted", "required_value": False, "weight": "critical"},
        {"id": "FW-002", "name": "water_access_not_interrupted", "field": "water_interrupted", "required_value": False, "weight": "critical"},
    ],
    "supply_chain": [
        {"id": "SC-001", "name": "critical_supply_available", "field": "critical_supply_gap", "required_value": False, "weight": "major"},
        {"id": "SC-002", "name": "alternate_supplier_identified", "field": "alternate_supplier_exists", "required_value": True, "weight": "minor"},
    ],
}


# ─────────────────────────────────────────────
# Condition Evaluator
# ─────────────────────────────────────────────

def _evaluate_rule(rule: dict, state: dict) -> dict:
    """Evaluate a single rule against a state dict. Returns pass/fail + reason."""
    field = rule.get("field")
    value = state.get(field)

    # Handle conditional rules
    cond = rule.get("conditional_on")
    if cond and not state.get(cond, False):
        return {"rule_id": rule["id"], "passed": True, "skipped": True, "reason": f"Condition '{cond}' not active"}

    if value is None:
        # Missing field = unknown = treat as degraded signal
        return {"rule_id": rule["id"], "passed": None, "unknown": True, "reason": f"Field '{field}' not provided"}

    passed = True
    reason = "OK"

    if "required_value" in rule:
        if value != rule["required_value"]:
            passed = False
            reason = f"'{field}' is {value}, expected {rule['required_value']}"

    if "required_min" in rule:
        if not isinstance(value, (int, float)) or value < rule["required_min"]:
            passed = False
            reason = f"'{field}' is {value}, minimum required is {rule['required_min']}"

    if "required_max" in rule:
        if not isinstance(value, (int, float)) or value > rule["required_max"]:
            passed = False
            reason = f"'{field}' is {value}, maximum allowed is {rule['required_max']}"

    return {
        "rule_id": rule["id"],
        "name": rule.get("name"),
        "description": rule.get("description", ""),
        "weight": rule.get("weight", "minor"),
        "passed": passed,
        "reason": reason,
    }


# ─────────────────────────────────────────────
# State Aggregator
# ─────────────────────────────────────────────

def _aggregate_results(results: list[dict], time_remaining_seconds: int | None = None) -> BoundaryState:
    """
    Aggregate rule results into a single BoundaryState.

    Logic:
      - Any critical failure (RC-001 through RC-006 or domain critical) → NON-ADMISSIBLE
      - Any unknown field on a critical rule → NON-ADMISSIBLE
        (unknown recoverability is non-admissible, not merely degraded)
      - If NON-ADMISSIBLE AND (execution gate fails OR time window collapsed) → NON-EXECUTABLE
      - Major failures only (no critical failures) → DEGRADED
      - All conditions met → CONTINUE
    """
    critical_failures = [
        r for r in results
        if not r.get("passed") and r.get("weight") in ("critical", "execution_gate") and not r.get("skipped")
    ]
    # Unknown on a critical rule = unestablished recoverability = NON-ADMISSIBLE
    critical_unknowns = [
        r for r in results
        if r.get("unknown") and r.get("weight") in ("critical", "execution_gate")
    ]
    major_failures = [
        r for r in results
        if not r.get("passed") and r.get("weight") == "major" and not r.get("skipped") and not r.get("unknown")
    ]

    has_non_admissible = bool(critical_failures or critical_unknowns)

    if has_non_admissible:
        # Upgrade to NON-EXECUTABLE if execution gate fails or time window collapsed
        gate_fail = any(
            r for r in results
            if r.get("weight") == "execution_gate" and not r.get("passed") and not r.get("skipped")
        )
        time_collapsed = (time_remaining_seconds is not None and time_remaining_seconds < 3600)
        if gate_fail or time_collapsed:
            return BoundaryState.NON_EXECUTABLE
        return BoundaryState.NON_ADMISSIBLE

    if major_failures:
        return BoundaryState.DEGRADED

    return BoundaryState.CONTINUE


# ─────────────────────────────────────────────
# Main Evaluation Entry Point
# ─────────────────────────────────────────────

def evaluate(case: dict) -> dict:
    """
    Main evaluation function.

    Input: case dict with:
      - domain: str (from SUPPORTED_DOMAINS)
      - state: dict of domain-specific fields
      - case_id (optional): str
      - label (optional): str
      - operator_id (optional): str

    Output: evaluation result dict with boundary_state and full trace.
    """
    eval_id   = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    domain    = case.get("domain", "unknown")
    state     = case.get("state", {})
    case_id   = case.get("case_id", eval_id)
    label     = case.get("label", "Unlabelled case")
    operator  = case.get("operator_id", "anonymous")

    logger.info(f"[{eval_id}] Evaluating case '{label}' in domain '{domain}'")

    all_results = []

    # Layer 1: Global Invariants
    for rule in GLOBAL_INVARIANTS:
        result = _evaluate_rule(rule, state)
        result["layer"] = "global_invariant"
        all_results.append(result)

    # Layer 2: Domain Rules
    domain_rules = DOMAIN_RULES.get(domain, [])
    if not domain_rules and domain != "unknown":
        logger.warning(f"[{eval_id}] No rules found for domain '{domain}'")

    for rule in domain_rules:
        result = _evaluate_rule(rule, state)
        result["layer"] = "domain"
        all_results.append(result)

    # Aggregate
    time_remaining = state.get("time_remaining_seconds")
    boundary_state = _aggregate_results(all_results, time_remaining)

    # Build failed conditions summary
    failed = [r for r in all_results if r.get("passed") is False and not r.get("skipped")]
    unknown = [r for r in all_results if r.get("unknown")]

    # Time-to-irreversibility
    tti = None
    if time_remaining is not None:
        tti = {
            "seconds_remaining": time_remaining,
            "hours_remaining": round(time_remaining / 3600, 2),
            "point_of_no_return_crossed": time_remaining <= 0,
            "margin_warning": time_remaining < 7200,  # < 2 hours
        }

    result_record = {
        "eval_id": eval_id,
        "case_id": case_id,
        "label": label,
        "domain": domain,
        "operator_id": operator,
        "timestamp": timestamp,
        "boundary_state": boundary_state.value,
        "failed_conditions": failed,
        "unknown_fields": unknown,
        "time_to_irreversibility": tti,
        "rule_trace": all_results,
        "passed_count": len([r for r in all_results if r.get("passed") is True]),
        "failed_count": len(failed),
        "unknown_count": len(unknown),
        "total_rules_evaluated": len(all_results),
    }

    logger.info(f"[{eval_id}] Result: {boundary_state.value} | Failed: {len(failed)} | Unknown: {len(unknown)}")

    return result_record


# ─────────────────────────────────────────────
# Continuous Re-gating
# ─────────────────────────────────────────────

class ContinuousGate:
    """
    Continuously re-evaluates a case at a given interval.
    Emits callbacks when state changes.
    """

    def __init__(self, case: dict, interval_seconds: int = 30, on_state_change=None):
        self.case = case
        self.interval = interval_seconds
        self.on_state_change = on_state_change
        self.last_state = None
        self.running = False
        self._history = []

    def start(self):
        import threading
        self.running = True
        thread = threading.Thread(target=self._loop, daemon=True)
        thread.start()
        logger.info(f"ContinuousGate started for case '{self.case.get('label')}' every {self.interval}s")

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            result = evaluate(self.case)
            current_state = result["boundary_state"]
            self._history.append(result)

            if current_state != self.last_state:
                logger.info(f"State change: {self.last_state} → {current_state}")
                if self.on_state_change:
                    self.on_state_change(self.last_state, current_state, result)
                self.last_state = current_state

            time.sleep(self.interval)

    def get_history(self):
        return self._history


# ─────────────────────────────────────────────
# Batch Evaluation
# ─────────────────────────────────────────────

def evaluate_batch(cases: list[dict]) -> list[dict]:
    """Evaluate a list of cases and return all results."""
    return [evaluate(c) for c in cases]


# ─────────────────────────────────────────────
# Path Enumeration
# ─────────────────────────────────────────────

def enumerate_paths(case: dict) -> dict:
    """
    Check known, fallback, and missing paths for a given case.
    Returns a path map with admissibility status for each.
    """
    paths = case.get("paths", {})
    result = {}
    for path_name, path_state in paths.items():
        sub_case = {**case, "state": {**case.get("state", {}), **path_state}, "label": f"{case.get('label')} [{path_name}]"}
        result[path_name] = evaluate(sub_case)
    return {
        "case_id": case.get("case_id"),
        "paths_evaluated": result,
        "admissible_paths":     [k for k, v in result.items() if v["boundary_state"] == BoundaryState.CONTINUE.value],
        "non_admissible_paths": [k for k, v in result.items() if v["boundary_state"] in [BoundaryState.NON_ADMISSIBLE.value, BoundaryState.NON_EXECUTABLE.value]],
    }


# ─────────────────────────────────────────────
# Cross-domain Propagation
# ─────────────────────────────────────────────

CROSS_DOMAIN_TRIGGERS = {
    "healthcare":      ["pharmacological", "transport", "identity", "finance"],
    "pharmacological": ["healthcare", "finance", "transport"],
    "housing":         ["finance", "identity", "healthcare"],
    "finance":         ["housing", "food_water", "identity"],
    "disaster":        ["housing", "transport", "healthcare", "communications", "food_water"],
    "infrastructure":  ["healthcare", "energy", "communications"],
}

def propagate_cross_domain(primary_result: dict, all_states: dict[str, dict]) -> dict:
    """
    If a domain evaluates as NON-ADMISSIBLE or NON-EXECUTABLE,
    automatically trigger evaluation on dependent domains.
    """
    domain = primary_result.get("domain")
    triggered = CROSS_DOMAIN_TRIGGERS.get(domain, [])
    propagated = {}
    for dep_domain in triggered:
        if dep_domain in all_states:
            dep_case = {"domain": dep_domain, "state": all_states[dep_domain], "label": f"Auto-propagated from {domain}"}
            propagated[dep_domain] = evaluate(dep_case)
    return {
        "primary_domain": domain,
        "primary_state": primary_result["boundary_state"],
        "propagated_evaluations": propagated,
        "cascading_non_admissible": [
            d for d, r in propagated.items()
            if r["boundary_state"] in [BoundaryState.NON_ADMISSIBLE.value, BoundaryState.NON_EXECUTABLE.value]
        ],
    }


if __name__ == "__main__":
    # Quick smoke test
    test_case = {
        "domain": "pharmacological",
        "label": "Benzodiazepine continuity check",
        "state": {
            "supply_days_remaining": 0,
            "prescriber_reachable": False,
            "abrupt_stop_risk": True,
            "dispensing_accessible": False,
            "taper_required": True,
            "taper_plan_exists": False,
            "interaction_flag": False,
            # Six recoverability conditions — all failing
            "recovery_path_exists": False,
            "recovery_path_reachable": False,
            "failure_detectable_in_time": True,
            "response_possible_in_time": False,
            "recovery_executable_in_time": False,
            "no_irreversible_transition_before_recovery": False,
            # Execution gates
            "human_authority_reachable": False,
            "time_remaining_seconds": 1800,
            "fallback_path_available": False,
            "override_active": False,
        }
    }
    result = evaluate(test_case)
    print(json.dumps(result, indent=2, default=str))
