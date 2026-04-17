from __future__ import annotations

from typing import List
import networkx as nx
from .models import CaseInput, RecoveryPath


def build_graph(case: CaseInput) -> nx.DiGraph:
    graph = nx.DiGraph()
    for entity in case.entities:
        graph.add_node(
            entity.name,
            type=entity.type,
            availability=entity.availability,
            reachable=entity.reachable,
            verifiable=entity.verifiable,
        )
    for dep in case.dependencies:
        graph.add_edge(
            dep.source,
            dep.target,
            kind=dep.kind,
            criticality=dep.criticality,
            fallback_exists=dep.fallback_exists,
        )
    return graph


def broken_dependencies(case: CaseInput) -> List[str]:
    entity_index = {entity.name: entity for entity in case.entities}
    broken: List[str] = []
    for dep in case.dependencies:
        source = entity_index.get(dep.source)
        target = entity_index.get(dep.target)
        if not source or not target:
            broken.append(f"Undefined dependency: {dep.source} -> {dep.target}")
            continue
        if not source.reachable or not target.reachable:
            broken.append(f"Reachability failure: {dep.source} -> {dep.target}")
        if not source.verifiable or not target.verifiable:
            broken.append(f"Verification failure: {dep.source} -> {dep.target}")
        if source.availability < 0.4 or target.availability < 0.4:
            broken.append(f"Availability collapse: {dep.source} -> {dep.target}")
        if dep.criticality >= 0.8 and not dep.fallback_exists and (source.availability < 0.7 or target.availability < 0.7):
            broken.append(f"Critical dependency without fallback: {dep.source} -> {dep.target}")
    return broken


def path_blockers(case: CaseInput, path: RecoveryPath) -> List[str]:
    entity_index = {entity.name: entity for entity in case.entities}
    blockers: List[str] = []
    for name in path.required_entities + path.required_resources:
        entity = entity_index.get(name)
        if not entity:
            blockers.append(f"Missing required entity/resource: {name}")
            continue
        if not entity.reachable:
            blockers.append(f"Unreachable: {name}")
        if not entity.verifiable:
            blockers.append(f"Unverifiable: {name}")
        if entity.availability < 0.5:
            blockers.append(f"Unavailable: {name}")
    return blockers
