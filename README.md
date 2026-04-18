Recoverability-Constrained Systems

Execution-Ready System for Admissible Action Under Irreversibility Constraints

Core Condition

A system may act only while recoverability can be established in time under real conditions.

If this cannot be established:

→ continuation is non-admissible
→ execution does not occur

What This Repository Is

This repository is the execution-ready implementation layer of the Recoverability-Constrained Systems framework.

It does not redefine the system.

It operationalizes:

admissibility
execution gating
failure prevention
real-time decision enforcement

under a single invariant.

Canonical Structure (Read in Order)

MI-001 — Master Index (Authoritative Structural Index)
https://doi.org/10.5281/zenodo.19583410

CE-004 — Minimal Executable Core and Adversarial Structural Closure
https://doi.org/10.5281/zenodo.19643189

CE-003 — Recoverability Condition for Admissible Action
https://doi.org/10.5281/zenodo.19637081

LD-002 — Recoverability-Constrained Admissibility Act (RCAA)
https://doi.org/10.5281/zenodo.19637946

EX-006 — Execution Closure Layer (Detection, Enforcement, and Actuation)
https://doi.org/10.5281/zenodo.19643413

PB-005 — Universal Admissibility Evaluation Standard (UAES)
https://doi.org/10.5281/zenodo.19644299

Run the System (Immediate Use)

To evaluate real-world decisions:

→ Open:

AEX/

or

Continuity_Engine/continuity_engine_local_v5/

Then follow:

INSTALL_AND_RUN.md

Execution Rule

A system may continue only if all of the following are established in time under real conditions:

state is known and current
detection occurs in time
action is executable in time
recovery is possible in time
dependencies are available
all paths are identifiable or blocked

If any condition cannot be established:

→ STOP / ESCALATE / CONTAIN

Unknown = non-admissible

Repository Structure
AEX — Admissibility Execution Layer (minimal runtime evaluator)
Continuity Engine — execution substrate (local runtime system)
Master Documents — authoritative framework records
RCCS — domain implementation + validated cases
Deployment / Maintenance — operational protocols
Preserved Source Bundles — source integrity

All components are governed by the same admissibility condition and must be interpreted together.

Use Paths
Understand the system

Read:

Master Index
Minimal Executable Core
Execution Closure Layer
Execute the system

Run:

AEX
Continuity Engine
Validate against reality

Review:

RCCS
failure cases
source bundles
System Behavior

If a system cannot:

detect in time
act in time
recover in time

→ execution does not occur

Canonical References

MI-001
https://doi.org/10.5281/zenodo.19583410

CE-004
https://doi.org/10.5281/zenodo.19643189

CE-003
https://doi.org/10.5281/zenodo.19637081

LD-002
https://doi.org/10.5281/zenodo.19637946

EX-006
https://doi.org/10.5281/zenodo.19643413

PB-005
https://doi.org/10.5281/zenodo.19644299

Final

This is not a framework for a domain.

It is a constraint on continuation itself.

If recoverability cannot be established in time under real conditions:

→ execution does not occur
