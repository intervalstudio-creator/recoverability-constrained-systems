# Boundary Full Platform v3.1

Boundary is an executable recoverability platform for continuation, escalation,
restriction, containment, and halt decisions under real conditions.

This all-in-one package includes:
- core decision engine
- execution layer
- runtime telemetry intake
- external integrations (email / SMS / incident / webhook / device)
- observability + dead-letter queue
- enterprise / NHS deployment profiles
- local web UI
- install scripts
- Electron desktop wrapper source
- GitHub auto-release workflow for installers

## Important

This is a **production-style integrated starter system**.
It is unified, runnable, and structured for GitHub deployment, but it is **not**
clinical certification, industrial control certification, or signed installer output.

## Quick start

### Mac / Linux
```bash
bash scripts/install_and_run.sh
```

### Windows
Run:
```bat
scripts\install_and_run.bat
```

Then open:
- http://127.0.0.1:8787

## Manual start
```bash
python api/server.py
```

## Key files
- `api/server.py`
- `app/index.html`
- `engine/execution_layer.py`
- `engine/external_actuation_observed.py`
- `configs/profiles/enterprise.json`
- `configs/profiles/nhs.json`
- `.github/workflows/release-installers.yml`

## Environment setup

Copy `.env.example` to `.env` and fill in real provider credentials if you want:
- SMTP email
- Twilio SMS
- PagerDuty incidents
- webhook / device actuation

If you leave credentials empty, the system still runs locally, but external actions
will fail gracefully and go to the dead-letter queue.
