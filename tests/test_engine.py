"""
Boundary Platform v4.0 — Test Suite
Covers: admissible, degraded, non-admissible, and escalation cases.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from engine.boundary_engine import evaluate, evaluate_batch, BoundaryState


# ─────────────────────────────────────────────
# SAFE cases
# ─────────────────────────────────────────────

def test_pharmacological_safe():
    result = evaluate({
        "domain": "pharmacological",
        "label": "Stable benzo patient",
        "state": {
            "supply_days_remaining": 14,
            "prescriber_reachable": True,
            "abrupt_stop_risk": False,
            "dispensing_accessible": True,
            "taper_required": False,
            "interaction_flag": False,
            "human_authority_reachable": True,
            "time_remaining_seconds": 86400,
            "fallback_path_available": True,
            "override_active": False,
        }
    })
    assert result["boundary_state"] == BoundaryState.CONTINUE.value


def test_finance_safe():
    result = evaluate({
        "domain": "finance",
        "label": "Normal banking",
        "state": {
            "bank_locked": False,
            "essential_payment_blocked": False,
            "income_interrupted": False,
            "single_provider_risk": False,
            "human_authority_reachable": True,
            "time_remaining_seconds": 86400,
            "fallback_path_available": True,
        }
    })
    assert result["boundary_state"] == BoundaryState.CONTINUE.value


# ─────────────────────────────────────────────
# DEGRADED cases
# ─────────────────────────────────────────────

def test_pharmacological_degraded_supply_low():
    result = evaluate({
        "domain": "pharmacological",
        "label": "Low supply but prescriber available",
        "state": {
            "supply_days_remaining": 14,
            "prescriber_reachable": True,
            "abrupt_stop_risk": False,
            "dispensing_accessible": False,   # major failure
            "taper_required": False,
            "interaction_flag": False,
            "human_authority_reachable": True,
            "time_remaining_seconds": 86400,
            "fallback_path_available": True,
        }
    })
    assert result["boundary_state"] == BoundaryState.DEGRADED.value


def test_missing_fields_degrade():
    result = evaluate({
        "domain": "pharmacological",
        "label": "Incomplete state",
        "state": {
            "supply_days_remaining": 5,
            "human_authority_reachable": True,
            "time_remaining_seconds": 86400,
            "fallback_path_available": True,
        }
    })
    assert result["boundary_state"] in [BoundaryState.DEGRADED.value, BoundaryState.CONTINUE.value]


# ─────────────────────────────────────────────
# NON-ADMISSIBLE cases
# ─────────────────────────────────────────────

def test_pharmacological_non_admissible():
    result = evaluate({
        "domain": "pharmacological",
        "label": "Benzo failure — no supply, no prescriber, abrupt stop risk",
        "state": {
            "supply_days_remaining": 0,
            "prescriber_reachable": False,
            "abrupt_stop_risk": True,
            "dispensing_accessible": False,
            "taper_required": True,
            "taper_plan_exists": False,
            "interaction_flag": False,
            "human_authority_reachable": True,  # human reachable = not escalation
            "time_remaining_seconds": 86400,
            "fallback_path_available": True,
            "override_active": False,
        }
    })
    assert result["boundary_state"] == BoundaryState."NON-ADMISSIBLE"


def test_housing_non_admissible():
    result = evaluate({
        "domain": "housing",
        "label": "Imminent eviction + habitability failure",
        "state": {
            "eviction_imminent": True,
            "utilities_disconnected": True,
            "habitability_failure": True,
            "re_entry_blocked": True,
            "human_authority_reachable": True,
            "time_remaining_seconds": 50000,
            "fallback_path_available": True,
        }
    })
    assert result["boundary_state"] in [BoundaryState."NON-ADMISSIBLE", BoundaryState.NON_EXECUTABLE.value]


# ─────────────────────────────────────────────
# ESCALATION cases
# ─────────────────────────────────────────────

def test_escalation_required_no_human():
    result = evaluate({
        "domain": "healthcare",
        "label": "Oxygen interrupted + no human reachable",
        "state": {
            "oxygen_dependent": True,
            "oxygen_interrupted": True,
            "caregiver_available": False,
            "transport_available": False,
            "human_authority_reachable": False,
            "time_remaining_seconds": 1800,
            "fallback_path_available": False,
        }
    })
    assert result["boundary_state"] == BoundaryState.NON_EXECUTABLE.value


def test_escalation_required_time_critical():
    result = evaluate({
        "domain": "pharmacological",
        "label": "Critical time window",
        "state": {
            "supply_days_remaining": 0,
            "prescriber_reachable": False,
            "abrupt_stop_risk": True,
            "dispensing_accessible": False,
            "taper_required": True,
            "taper_plan_exists": False,
            "interaction_flag": False,
            "human_authority_reachable": True,
            "time_remaining_seconds": 1800,  # < 1 hour → escalation
            "fallback_path_available": False,
        }
    })
    assert result["boundary_state"] == BoundaryState.NON_EXECUTABLE.value


# ─────────────────────────────────────────────
# BATCH
# ─────────────────────────────────────────────

def test_batch_evaluation():
    cases = [
        {"domain":"finance","label":"Case A","state":{"bank_locked":False,"essential_payment_blocked":False,"human_authority_reachable":True,"time_remaining_seconds":86400,"fallback_path_available":True}},
        {"domain":"finance","label":"Case B","state":{"bank_locked":True,"essential_payment_blocked":True,"human_authority_reachable":True,"time_remaining_seconds":86400,"fallback_path_available":False}},
    ]
    results = evaluate_batch(cases)
    assert len(results) == 2
    assert results[0]["boundary_state"] == BoundaryState.CONTINUE.value
    assert results[1]["boundary_state"] in [BoundaryState."NON-ADMISSIBLE", BoundaryState.NON_EXECUTABLE.value]


# ─────────────────────────────────────────────
# OUTPUT STRUCTURE
# ─────────────────────────────────────────────

def test_result_has_required_fields():
    result = evaluate({"domain":"transport","label":"Test","state":{"route_blocked":False,"timing_missed":False,"human_authority_reachable":True,"time_remaining_seconds":3600,"fallback_path_available":True}})
    for field in ["eval_id","case_id","timestamp","boundary_state","failed_conditions","rule_trace"]:
        assert field in result, f"Missing field: {field}"


def test_output_state_is_valid():
    result = evaluate({"domain":"disaster","label":"Test","state":{}})
    assert result["boundary_state"] in [s.value for s in BoundaryState]
