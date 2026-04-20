# Boundary Full Platform v3.2

Boundary is an autonomous recoverability-constrained execution platform.

This package includes:
- core decision engine
- bounded execution layer
- observability and audit logging
- external actuation connectors
- automatic event-driven execution
- continuity workflows for identity, finance, transport, and disaster cases
- local UI
- install scripts

## New: Pharmacological Systems Layer

Boundary now includes a pharmacological and medication continuity layer extending recoverability constraints to substance-dependent systems.

This defines when medication use, continuation, tapering, or interruption becomes non-admissible under real conditions.

Includes:

- Substance, Material, and Interval Systems  
- Unified Pharmacological Architecture  
- Benzodiazepine Protocol (dependency and withdrawal case)

Folder:
Domain_Pharmacological_Systems/

Authoritative records:

- Substance, Material, Interval Systems  
https://doi.org/10.5281/zenodo.19664442  

- Benzodiazepine Protocol  
https://doi.org/10.5281/zenodo.19664722  

- Pharmacological Systems Architecture  
https://doi.org/10.5281/zenodo.19664810  

## Quick start

### Windows
scripts\install_and_run.bat

### Mac / Linux
bash scripts/install_and_run.sh

Then open:
- `app/index.html`

Keep the backend running at:
- `http://127.0.0.1:8787`

## Main endpoints
- `POST /api/events`
- `POST /api/auto/start`
- `POST /api/auto/stop`
- `GET /api/auto/status`
- `GET /api/observability`

## Important
This build includes autonomous execution and continuity scaffolding.
It does not include live bank, government, telecom, or hospital credentials.
