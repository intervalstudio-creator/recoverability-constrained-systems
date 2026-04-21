"""
Boundary API v4.0
FastAPI server — runs at http://127.0.0.1:8787

Core endpoints:
  POST /api/evaluate              - single case evaluation
  POST /api/evaluate/batch        - batch evaluation
  POST /api/evaluate/paths        - path enumeration
  POST /api/evaluate/propagate    - cross-domain propagation
  POST /api/events                - event-driven evaluation trigger
  POST /api/escalation/trigger    - manual escalation trigger
  POST /api/override              - log an override
  POST /api/auto/start            - start continuous re-gating
  POST /api/auto/stop             - stop continuous re-gating
  GET  /api/auto/status           - continuous gate status
  GET  /api/observability         - dashboard summary
  GET  /api/decisions             - decision log query
  GET  /api/residue               - unresolved residue
  GET  /api/timeline/{case_id}    - timeline reconstruction
  GET  /api/incidents             - incident library search
  POST /api/incidents/save        - save to incident library
  GET  /api/audit/export          - full audit export
  GET  /api/domains               - list supported domains
  GET  /api/templates             - case templates library
  GET  /api/health                - health check

Feature endpoints (v4.1):
  POST /api/monitor/subject       - evaluate a person across all domains
  POST /api/monitor/population    - evaluate a cohort simultaneously
  GET  /api/clock/all             - all active PNR clocks
  GET  /api/clock/critical        - clocks in critical/crossed state
  POST /api/clock/register        - register a new PNR clock
  POST /api/override/formal       - create formal accountability record
  GET  /api/override/report       - generate accountability report
  GET  /api/plain/domains         - plain-language domain selector
  GET  /api/plain/questions/{dom} - plain-language question tree
  POST /api/plain/evaluate        - evaluate from plain-language answers
  POST /api/corpus/export         - export research corpus
  GET  /api/corpus/patterns       - detect patterns in incident library
  POST /api/corpus/regulatory     - generate regulatory submission pack
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Optional
import uuid
import json
from datetime import datetime, timezone

from engine.boundary_engine import (
    evaluate, evaluate_batch, enumerate_paths,
    propagate_cross_domain, ContinuousGate, SUPPORTED_DOMAINS, BoundaryState
)
from observability.observability import (
    log_decision, log_override, log_residue, save_incident,
    get_decisions, get_unresolved_residue, reconstruct_timeline,
    search_incidents, get_dashboard_summary, get_overrides
)
from engine.continuity_monitor import (
    ContinuityObject, evaluate_continuity_object, evaluate_population
)
from engine.ponr_clock import (
    registry as clock_registry, compute_timing_from_evaluation, THRESHOLDS
)
from engine.override_accountability import (
    create_override_record, generate_accountability_report,
    get_all_override_records, verify_record_integrity
)
from engine.plain_language import (
    build_case_from_answers, get_question_tree, get_domain_selector,
    explain_result_plain, QUESTION_TREES
)
from engine.research_corpus import (
    detect_patterns, export_corpus_json, export_corpus_csv,
    generate_regulatory_pack, anonymise_record
)
from engine.population_view import (
    Cohort, evaluate_cohort, build_cohort_from_list, compare_cohort_snapshots
)

app = FastAPI(
    title="Boundary Platform API v4.0",
    description="Recoverability-Constrained Execution Platform — visibility and escalation engine",
    version="4.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active continuous gates registry
active_gates: dict[str, ContinuousGate] = {}


# ─────────────────────────────────────────────
# Request Models
# ─────────────────────────────────────────────

class CaseRequest(BaseModel):
    domain: str
    label: Optional[str] = "Unlabelled case"
    case_id: Optional[str] = None
    operator_id: Optional[str] = "anonymous"
    state: dict[str, Any]
    paths: Optional[dict[str, dict]] = None

class BatchRequest(BaseModel):
    cases: list[CaseRequest]

class PropagateRequest(BaseModel):
    primary_case: CaseRequest
    all_states: dict[str, dict[str, Any]]

class EscalationRequest(BaseModel):
    case_id: str
    domain: str
    reason: str
    operator_id: Optional[str] = "anonymous"
    contact_method: Optional[str] = "system"

class OverrideRequest(BaseModel):
    case_id: str
    operator_id: str
    reason: str
    original_state: str

class AutoStartRequest(BaseModel):
    case: CaseRequest
    interval_seconds: Optional[int] = 30

class IncidentSaveRequest(BaseModel):
    evaluation_result: dict
    notes: Optional[str] = ""

class EventRequest(BaseModel):
    event_type: str
    domain: str
    case_id: Optional[str] = None
    state: dict[str, Any]
    operator_id: Optional[str] = "system"


# ─────────────────────────────────────────────
# Evaluation Endpoints
# ─────────────────────────────────────────────

@app.post("/api/evaluate")
async def evaluate_case(req: CaseRequest):
    case = req.model_dump()
    result = evaluate(case)
    log_decision(result)
    if result["boundary_state"] in ["NON-ADMISSIBLE", "NON-EXECUTABLE"]:
        log_residue(result["case_id"], "non_admissible", f"Case evaluated {result['boundary_state']}", metadata=result)
    return result


@app.post("/api/evaluate/batch")
async def evaluate_cases_batch(req: BatchRequest):
    cases = [c.model_dump() for c in req.cases]
    results = evaluate_batch(cases)
    for r in results:
        log_decision(r)
    return {"results": results, "total": len(results)}


@app.post("/api/evaluate/paths")
async def evaluate_case_paths(req: CaseRequest):
    case = req.model_dump()
    if not case.get("paths"):
        raise HTTPException(status_code=400, detail="No paths provided in request")
    result = enumerate_paths(case)
    return result


@app.post("/api/evaluate/propagate")
async def evaluate_propagation(req: PropagateRequest):
    primary_result = evaluate(req.primary_case.model_dump())
    log_decision(primary_result)
    propagation = propagate_cross_domain(primary_result, req.all_states)
    for dep_result in propagation["propagated_evaluations"].values():
        log_decision(dep_result)
    return propagation


# ─────────────────────────────────────────────
# Event-Driven Endpoint
# ─────────────────────────────────────────────

@app.post("/api/events")
async def handle_event(req: EventRequest):
    case = {
        "domain": req.domain,
        "case_id": req.case_id or str(uuid.uuid4()),
        "label": f"Event: {req.event_type}",
        "operator_id": req.operator_id,
        "state": req.state,
    }
    result = evaluate(case)
    log_decision(result)
    return {
        "event_type": req.event_type,
        "triggered_at": datetime.now(timezone.utc).isoformat(),
        "evaluation": result,
    }


# ─────────────────────────────────────────────
# Escalation
# ─────────────────────────────────────────────

@app.post("/api/escalation/trigger")
async def trigger_escalation(req: EscalationRequest):
    residue_id = log_residue(
        req.case_id,
        "escalation_triggered",
        f"Manual escalation: {req.reason}",
        metadata={"domain": req.domain, "operator_id": req.operator_id, "contact_method": req.contact_method}
    )
    return {
        "escalation_id": residue_id,
        "case_id": req.case_id,
        "domain": req.domain,
        "reason": req.reason,
        "status": "ESCALATION_LOGGED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Escalation logged. A responsible human authority must be reached.",
    }


# ─────────────────────────────────────────────
# Override Accountability
# ─────────────────────────────────────────────

@app.post("/api/override")
async def log_override_endpoint(req: OverrideRequest):
    override_id = log_override(req.case_id, req.operator_id, req.reason, req.original_state)
    return {
        "override_id": override_id,
        "case_id": req.case_id,
        "operator_id": req.operator_id,
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "warning": "Override logged permanently. Identity, reason, and timing are recorded.",
    }


# ─────────────────────────────────────────────
# Continuous Re-gating
# ─────────────────────────────────────────────

@app.post("/api/auto/start")
async def start_auto(req: AutoStartRequest):
    gate_id = req.case.case_id or str(uuid.uuid4())

    def on_change(old_state, new_state, result):
        log_decision(result)
        if new_state in ["NON-ADMISSIBLE", "NON-EXECUTABLE"]:
            log_residue(gate_id, "state_change_residue",
                        f"State changed from {old_state} to {new_state}",
                        metadata=result)

    gate = ContinuousGate(req.case.model_dump(), req.interval_seconds, on_change)
    gate.start()
    active_gates[gate_id] = gate
    return {"gate_id": gate_id, "status": "STARTED", "interval_seconds": req.interval_seconds}


@app.post("/api/auto/stop")
async def stop_auto(gate_id: str):
    gate = active_gates.get(gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate not found")
    gate.stop()
    del active_gates[gate_id]
    return {"gate_id": gate_id, "status": "STOPPED"}


@app.get("/api/auto/status")
async def auto_status():
    return {
        "active_gates": list(active_gates.keys()),
        "count": len(active_gates),
    }


# ─────────────────────────────────────────────
# Observability
# ─────────────────────────────────────────────

@app.get("/api/observability")
async def observability_dashboard():
    return get_dashboard_summary()


@app.get("/api/decisions")
async def query_decisions(
    domain: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = Query(default=50, le=500)
):
    return {"decisions": get_decisions(domain=domain, state=state, limit=limit)}


@app.get("/api/residue")
async def get_residue():
    return {"residue": get_unresolved_residue()}


@app.get("/api/timeline/{case_id}")
async def get_timeline(case_id: str):
    return reconstruct_timeline(case_id)


@app.get("/api/incidents")
async def query_incidents(
    domain: Optional[str] = None,
    state: Optional[str] = None,
    text: Optional[str] = None
):
    return {"incidents": search_incidents(domain=domain, state=state, text=text)}


@app.post("/api/incidents/save")
async def save_to_incidents(req: IncidentSaveRequest):
    incident_id = save_incident(req.evaluation_result, req.notes)
    return {"incident_id": incident_id, "saved": True}


@app.get("/api/audit/export")
async def export_audit():
    summary = get_dashboard_summary()
    decisions = get_decisions(limit=500)
    residue = get_unresolved_residue()
    overrides = get_overrides()
    return {
        "export_generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "decisions": decisions,
        "unresolved_residue": residue,
        "overrides": overrides,
    }


# ─────────────────────────────────────────────
# Meta
# ─────────────────────────────────────────────

@app.get("/api/domains")
async def list_domains():
    return {"domains": SUPPORTED_DOMAINS}


@app.get("/api/templates")
async def list_templates():
    return {
        "templates": [
            {
                "id": "benzo-withdrawal",
                "label": "Benzodiazepine withdrawal continuity",
                "domain": "pharmacological",
                "state": {
                    "supply_days_remaining": 0,
                    "prescriber_reachable": False,
                    "abrupt_stop_risk": True,
                    "dispensing_accessible": False,
                    "taper_required": True,
                    "taper_plan_exists": False,
                    "interaction_flag": False,
                    "human_authority_reachable": False,
                    "time_remaining_seconds": 14400,
                    "fallback_path_available": False,
                    "override_active": False,
                },
            },
            {
                "id": "hospital-transport-failure",
                "label": "Missed hospital transport — critical appointment",
                "domain": "healthcare",
                "state": {
                    "critical_appointment_missed": True,
                    "transport_available": False,
                    "caregiver_available": False,
                    "human_authority_reachable": True,
                    "time_remaining_seconds": 7200,
                    "fallback_path_available": False,
                    "override_active": False,
                },
            },
            {
                "id": "bank-lockout",
                "label": "Bank account locked — essential payment blocked",
                "domain": "finance",
                "state": {
                    "bank_locked": True,
                    "essential_payment_blocked": True,
                    "income_interrupted": True,
                    "single_provider_risk": True,
                    "human_authority_reachable": True,
                    "time_remaining_seconds": 86400,
                    "fallback_path_available": False,
                    "override_active": False,
                },
            },
            {
                "id": "identity-loss",
                "label": "Identity documents lost — access recovery needed",
                "domain": "identity",
                "state": {
                    "id_document_available": False,
                    "access_recovery_available": False,
                    "payroll_identity_intact": False,
                    "institution_portability_gap": True,
                    "human_authority_reachable": True,
                    "time_remaining_seconds": 172800,
                    "fallback_path_available": True,
                    "override_active": False,
                },
            },
            {
                "id": "oxygen-interruption",
                "label": "Oxygen-dependent patient — supply interrupted",
                "domain": "healthcare",
                "state": {
                    "oxygen_dependent": True,
                    "oxygen_interrupted": True,
                    "caregiver_available": False,
                    "transport_available": False,
                    "human_authority_reachable": False,
                    "time_remaining_seconds": 1800,
                    "fallback_path_available": False,
                    "override_active": False,
                },
            },
            {
                "id": "eviction-imminent",
                "label": "Imminent eviction — shelter continuity at risk",
                "domain": "housing",
                "state": {
                    "eviction_imminent": True,
                    "utilities_disconnected": True,
                    "habitability_failure": False,
                    "re_entry_blocked": True,
                    "human_authority_reachable": True,
                    "time_remaining_seconds": 43200,
                    "fallback_path_available": False,
                    "override_active": False,
                },
            },
            {
                "id": "disaster-evacuation",
                "label": "Disaster — evacuation window closing",
                "domain": "disaster",
                "state": {
                    "evacuation_window_closed": False,
                    "shelter_assigned": False,
                    "comms_collapsed": True,
                    "human_authority_reachable": True,
                    "time_remaining_seconds": 3600,
                    "fallback_path_available": True,
                    "override_active": False,
                },
            },
        ]
    }


@app.get("/api/health")
async def health():
    return {
        "status": "OK",
        "version": "4.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_gates": len(active_gates),
        "active_clocks": clock_registry.summary()["total_clocks"],
    }


# ═════════════════════════════════════════════
# FEATURE 1: Cross-Institutional Continuity Monitor
# ═════════════════════════════════════════════

class SubjectDomainRequest(BaseModel):
    subject_id: str
    label: Optional[str] = ""
    domains: dict[str, dict[str, Any]]

class PopulationRequest(BaseModel):
    subjects: list[SubjectDomainRequest]

@app.post("/api/monitor/subject")
async def monitor_subject(req: SubjectDomainRequest):
    """Evaluate a person across all their active domains simultaneously."""
    obj = ContinuityObject(req.subject_id, req.label or req.subject_id)
    for domain, state in req.domains.items():
        obj.set_domain_state(domain, state)
    result = evaluate_continuity_object(obj)
    for domain_result in result["domain_results"].values():
        log_decision(domain_result)
    return result

@app.post("/api/monitor/population")
async def monitor_population(req: PopulationRequest):
    """Evaluate a cohort of subjects simultaneously."""
    subjects = [
        {"subject_id": s.subject_id, "label": s.label, "domains": s.domains}
        for s in req.subjects
    ]
    cohort = build_cohort_from_list(str(uuid.uuid4()), "API Population Request", subjects)
    return evaluate_cohort(cohort)


# ═════════════════════════════════════════════
# FEATURE 2: Point-of-No-Return Clock
# ═════════════════════════════════════════════

class ClockRegisterRequest(BaseModel):
    case_id: str
    label: str
    domain: str
    seconds_to_irreversibility: Optional[float] = None
    detection_window_seconds: Optional[float] = None
    response_window_seconds: Optional[float] = None
    recovery_window_seconds: Optional[float] = None

class ClockUpdateRequest(BaseModel):
    case_id: str
    seconds_remaining: float

@app.post("/api/clock/register")
async def register_clock(req: ClockRegisterRequest):
    clock = clock_registry.register(
        req.case_id, req.label, req.domain,
        req.seconds_to_irreversibility,
        req.detection_window_seconds,
        req.response_window_seconds,
        req.recovery_window_seconds,
    )
    return clock.to_display()

@app.post("/api/clock/update")
async def update_clock(req: ClockUpdateRequest):
    threshold_crossed = clock_registry.update(req.case_id, req.seconds_remaining)
    clock = clock_registry.get(req.case_id)
    if not clock:
        raise HTTPException(status_code=404, detail="Clock not found")
    result = clock.to_display()
    result["threshold_just_crossed"] = threshold_crossed
    return result

@app.get("/api/clock/all")
async def get_all_clocks():
    return {
        "clocks": clock_registry.get_all_display(),
        "summary": clock_registry.summary(),
    }

@app.get("/api/clock/critical")
async def get_critical_clocks():
    return {
        "critical_clocks": clock_registry.get_critical(),
        "crossed_clocks": clock_registry.get_crossed(),
    }


# ═════════════════════════════════════════════
# FEATURE 3: Override Accountability Record
# ═════════════════════════════════════════════

class FormalOverrideRequest(BaseModel):
    case_id: str
    domain: str
    boundary_state: str
    operator_id: str
    operator_role: str
    reason: str
    acknowledged_risk: str
    authorising_authority: str
    evaluation_result: Optional[dict] = None
    metadata: Optional[dict] = None

class AccountabilityReportRequest(BaseModel):
    case_id: Optional[str] = None
    domain: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None

@app.post("/api/override/formal")
async def create_formal_override(req: FormalOverrideRequest):
    try:
        record = create_override_record(
            case_id=req.case_id,
            domain=req.domain,
            boundary_state=req.boundary_state,
            operator_id=req.operator_id,
            operator_role=req.operator_role,
            reason=req.reason,
            acknowledged_risk=req.acknowledged_risk,
            authorising_authority=req.authorising_authority,
            evaluation_result=req.evaluation_result or {},
            metadata=req.metadata,
        )
        return record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/override/report")
async def get_accountability_report(req: AccountabilityReportRequest):
    return generate_accountability_report(
        case_id=req.case_id,
        domain=req.domain,
        from_date=req.from_date,
        to_date=req.to_date,
    )

@app.get("/api/override/records")
async def list_override_records(domain: Optional[str] = None):
    return {"records": get_all_override_records(domain=domain)}


# ═════════════════════════════════════════════
# FEATURE 4: Plain-Language Case Builder
# ═════════════════════════════════════════════

class PlainAnswersRequest(BaseModel):
    domain: str
    answers: dict[str, Any]
    label: Optional[str] = ""

@app.get("/api/plain/domains")
async def plain_domain_selector():
    return {"domains": get_domain_selector()}

@app.get("/api/plain/questions/{domain}")
async def plain_questions(domain: str):
    tree = get_question_tree(domain)
    if not tree:
        raise HTTPException(status_code=404, detail=f"No question tree for domain '{domain}'")
    return tree

@app.post("/api/plain/evaluate")
async def plain_evaluate(req: PlainAnswersRequest):
    case = build_case_from_answers(req.domain, req.answers, req.label)
    result = evaluate(case)
    log_decision(result)
    plain_explanation = explain_result_plain(result)
    return {
        "evaluation": result,
        "plain_explanation": plain_explanation,
        "translated_state": case["state"],
    }


# ═════════════════════════════════════════════
# FEATURE 5: Research Corpus
# ═════════════════════════════════════════════

class CorpusExportRequest(BaseModel):
    anonymise: bool = True
    domain: Optional[str] = None

class RegulatoryPackRequest(BaseModel):
    domain: Optional[str] = None

@app.get("/api/corpus/patterns")
async def corpus_patterns():
    records = get_decisions(limit=500)
    return detect_patterns(records)

@app.post("/api/corpus/export")
async def corpus_export(req: CorpusExportRequest):
    records = get_decisions(domain=req.domain, limit=500)
    if req.anonymise:
        records = [anonymise_record(r) for r in records]
    patterns = detect_patterns(records)
    return {
        "corpus_id": str(uuid.uuid4()),
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "anonymised": req.anonymise,
        "total_records": len(records),
        "records": records,
        "patterns": patterns,
    }

@app.post("/api/corpus/regulatory")
async def corpus_regulatory(req: RegulatoryPackRequest):
    records = get_decisions(limit=500)
    return generate_regulatory_pack(records, domain=req.domain)


# ═════════════════════════════════════════════
# FEATURE 6: Population-Level Continuity View
# ═════════════════════════════════════════════

class CohortRequest(BaseModel):
    cohort_id: Optional[str] = None
    label: str
    context: Optional[str] = ""
    subjects: list[SubjectDomainRequest]

@app.post("/api/cohort/evaluate")
async def evaluate_cohort_endpoint(req: CohortRequest):
    subjects = [
        {"subject_id": s.subject_id, "label": s.label, "domains": s.domains}
        for s in req.subjects
    ]
    cohort = build_cohort_from_list(
        req.cohort_id or str(uuid.uuid4()),
        req.label,
        subjects,
    )
    cohort.context = req.context or ""
    return evaluate_cohort(cohort)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8787, log_level="info")
