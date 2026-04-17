from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field

AdmissibilityClass = Literal[
    "admissible",
    "degraded",
    "restricted",
    "containment-required",
    "halt-required",
    "restore-required",
    "non-executable",
    "uncertifiable",
]


class Entity(BaseModel):
    name: str
    type: Literal[
        "human",
        "team",
        "institution",
        "subsystem",
        "device",
        "resource",
        "external_dependency",
        "interface",
    ] = "human"
    availability: float = Field(default=1.0, ge=0.0, le=1.0)
    reachable: bool = True
    verifiable: bool = True


class Dependency(BaseModel):
    source: str
    target: str
    kind: Literal[
        "dependency",
        "authority",
        "communication",
        "control",
        "resource",
        "restoration",
        "fallback",
    ] = "dependency"
    criticality: float = Field(default=0.5, ge=0.0, le=1.0)
    fallback_exists: bool = False


class Interval(BaseModel):
    name: Literal[
        "detection",
        "interpretation",
        "decision",
        "response",
        "enforcement",
        "restoration",
        "verification",
    ]
    current_minutes: float = Field(ge=0.0)
    max_minutes: float = Field(gt=0.0)


class RecoveryPath(BaseModel):
    name: str
    executable: bool = True
    bounded_minutes: float = Field(gt=0.0)
    required_entities: List[str] = Field(default_factory=list)
    required_resources: List[str] = Field(default_factory=list)
    degraded_mode_valid: bool = False


class Signal(BaseModel):
    name: str
    source: str
    current_value: str | float | int | bool
    verifiable: bool = True
    stale: bool = False
    conflicted: bool = False
    observed_minutes_ago: float = Field(default=0.0, ge=0.0)
    max_age_minutes: float = Field(default=60.0, gt=0.0)


class DownstreamSystem(BaseModel):
    name: str
    dependency_on_case: float = Field(default=0.5, ge=0.0, le=1.0)
    irreversible_if_invalid: bool = False


class CertificateDependency(BaseModel):
    name: str
    required_for: Literal[
        "local_execution",
        "remote_api",
        "public_https",
        "code_signing",
        "client_auth",
        "data_exchange",
    ] = "remote_api"
    status: Literal["valid", "missing", "expired", "revoked", "unreachable", "unknown"] = "unknown"
    renewable_in_time: bool = False
    fallback_exists: bool = False
    continuity_critical: bool = True
    expires_in_days: Optional[float] = None


class ConnectivityProfile(BaseModel):
    mode: Literal["offline", "online", "degraded", "unknown"] = "unknown"
    network_required_for_primary_path: bool = False
    network_required_for_local_use: bool = False
    fallback_local_mode_available: bool = True
    remote_sync_enabled: bool = False
    certificate_dependencies: List[CertificateDependency] = Field(default_factory=list)


class CaseInput(BaseModel):
    title: str
    domain: str
    summary: str
    irreversible_outcomes: List[str]
    time_to_irreversibility_minutes: float = Field(gt=0.0)
    entities: List[Entity]
    dependencies: List[Dependency]
    intervals: List[Interval]
    recovery_paths: List[RecoveryPath]
    pressure: float = Field(default=0.2, ge=0.0, le=1.0)
    resonance: float = Field(default=0.1, ge=0.0, le=1.0)
    future_state_preserved: bool = True
    notes: Optional[str] = None
    signal_sources: List[Signal] = Field(default_factory=list)
    downstream_systems: List[DownstreamSystem] = Field(default_factory=list)
    connectivity: ConnectivityProfile = Field(default_factory=ConnectivityProfile)


class PathEvaluation(BaseModel):
    name: str
    valid: bool
    bounded_minutes: float
    margin_minutes: float
    degraded_mode_valid: bool
    blockers: List[str] = Field(default_factory=list)
    last_admissible_action_minutes: float
    point_of_no_return_minutes: float


class IAFResult(BaseModel):
    restoration_reachable: bool
    propagation_bounded: bool
    interval_continuity: bool
    dependency_integrity: bool
    future_state_preserved: bool
    trajectory_valid: bool
    viable_recovery_path_count: int
    blocked_recovery_path_count: int
    path_evaluations: List[PathEvaluation]
    irreversibility_budget: float
    point_of_no_return_minutes: float
    last_admissible_action: str
    proof_lines: List[str]
    truth_integrity_ok: bool
    authority_reachable: bool
    authority_reason: str
    propagated_failures: List[str]
    reasoning: List[str]
    offline_mode_engaged: bool = False
    local_execution_admissible: bool = True
    network_dependent_execution_admissible: bool = True
    connection_reason: str = ""
    certificate_reason: str = ""
    valid_certificates: int = 0
    broken_certificates: int = 0


class EvaluationResult(BaseModel):
    case_title: str
    domain: str
    admissibility_class: AdmissibilityClass
    reasons: List[str]
    required_actions: List[str]
    recovery_reachable: bool
    timing_margin_minutes: float
    broken_dependencies: List[str]
    report_timestamp: str
    iaf: IAFResult
