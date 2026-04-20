Boundary Full Platform v3.2

Boundary is a recoverability-constrained system for detecting when continuation becomes non-recoverable in time under real conditions and signaling escalation.

It implements a universal execution constraint across human, institutional, computational, artificial intelligence, robotic, and hybrid systems.

Core Principle

A system may evaluate, simulate, or recommend without restriction.

A system may only execute where recoverability can be established in time under real conditions as sufficient to prevent irreversible transition.

If recoverability cannot be established:

continuation is non-admissible
execution does not occur
Platform Overview

This package includes:

core evaluation engine
bounded execution constraint layer
observability and audit logging
external connectors (non-authoritative)
automatic event-driven evaluation
continuity workflows for identity, finance, transport, and disaster cases
local UI
install scripts
System Structure

Boundary is aligned with three layers:

1. Master Index (Authoritative Structure)

Defines the complete, non-fragmentable architecture of the framework.

DOI: https://doi.org/10.5281/zenodo.19583410

2. Execution Constraint (Foundational)

Recoverability-Constrained Execution — Universal Constraint on Autonomous, Human, and Hybrid Systems (Closed Form)

Defines when execution is admissible.

Key properties:

Unknown = non-admissible
Admissibility is binary
Execution requires recoverability in time
Evaluation is unrestricted
3. Unified Architecture (System Layer)

Recoverability-Constrained Systems — Universal Execution Constraint and Cross-Domain Continuity Architecture (Ultimate Unified Closed Form)

Defines how the constraint is applied across domains.

New: Pharmacological Systems Layer

Boundary includes a pharmacological and medication continuity layer extending recoverability constraints to substance-dependent systems.

This defines when medication use, continuation, tapering, or interruption becomes non-admissible under real conditions.

Includes:

Substance, Material, and Interval Systems
Unified Pharmacological Architecture
Benzodiazepine Protocol (dependency and withdrawal case)

Folder: Domain_Pharmacological_Systems/

Authoritative records:

Substance, Material, Interval Systems
https://doi.org/10.5281/zenodo.19664442
Benzodiazepine Protocol
https://doi.org/10.5281/zenodo.19664722
Pharmacological Systems Architecture
https://doi.org/10.5281/zenodo.19664810
Runtime Behavior

Boundary evaluates real-world conditions and outputs:

CONTINUE
DEGRADED
NON-ADMISSIBLE
NON-EXECUTABLE

Where non-admissible:

escalation is required
continuation must not proceed
Execution Model

Execution is permitted only if all conditions hold:

recovery path exists
recovery path is reachable
failure can be detected in time
response can occur in time
recovery can be executed in time
no irreversible transition occurs before recovery

If any condition fails:

execution is non-admissible
Positioning

Boundary is a detection and escalation system.

It does NOT:

provide medical advice
replace clinicians
autonomously control real-world systems

It identifies when continuation becomes non-recoverable and signals escalation.

Quick start
Windows

scripts\install_and_run.bat

Mac / Linux

bash scripts/install_and_run.sh

Then open:

app/index.html

Keep the backend running at:

http://127.0.0.1:8787
Main endpoints
POST /api/events
POST /api/auto/start
POST /api/auto/stop
GET /api/auto/status
GET /api/observability
Important

This build includes evaluation, detection, and continuity scaffolding.

It does not include live bank, government, telecom, or hospital credentials, and does not execute real-world actions.

Summary

Boundary enforces a single condition:

A system may act only while recovery remains possible.

If recovery cannot be established:

continuation does not occur.
