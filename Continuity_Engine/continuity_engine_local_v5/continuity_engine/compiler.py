from __future__ import annotations

from typing import Dict
from .models import CaseInput


def compile_case(case: CaseInput) -> Dict[str, object]:
    entity_index = {entity.name: entity for entity in case.entities}
    dependency_pairs = [(dep.source, dep.target, dep.kind, dep.criticality) for dep in case.dependencies]
    interval_map = {interval.name: interval for interval in case.intervals}
    return {
        "case": case,
        "entity_index": entity_index,
        "dependency_pairs": dependency_pairs,
        "interval_map": interval_map,
    }
