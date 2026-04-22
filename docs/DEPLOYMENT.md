# Boundary Deployment Guide

---

## Local deployment (default)

### Requirements

- Python 3.10 or later
- Any modern web browser

### Windows

```
scripts\install_and_run.bat
```

This installs dependencies, starts the backend at `http://127.0.0.1:8787`, and opens the UI.

### Mac / Linux

```bash
bash scripts/install_and_run.sh
```

### Manual start

```bash
pip install -r requirements.txt
python -m uvicorn api.server:app --host 127.0.0.1 --port 8787 --reload
```

Then open `web/index.html` in your browser.

---

## Offline mode

`web/index.html` works without any backend. The full evaluation engine runs in the browser as a JavaScript mirror of the Python engine. All four states are available. Results are stored in session storage.

The offline banner appears automatically when the backend is unreachable. All UI functions that require the backend (audit export, accountability reports, corpus patterns) indicate their status clearly.

---

## Institutional deployment

### NHS / Hospital

Deploy the backend on a local server within the institution's network. Open `web/index.html` from any browser on the same network. No internet connection required once deployed.

Set the backend URL in `web/index.html`:

```javascript
const API_BASE = "http://your-server-ip:8787";
```

For ward or department use, consider assigning a bookmark or shortcut to the UI file.

### Care home

Same as hospital. Deploy on a local machine or server. Access from any device on the local network. For single-device use, run the install script and use the local UI directly.

### Field / emergency deployment

Use the portable mode: copy the full `boundary-v4/` folder to a USB drive or laptop. Run `install_and_run.bat` or `install_and_run.sh` on arrival. The system runs entirely locally with no network requirement.

### NGO / settlement

Same as field deployment. Multiple operators can use the same backend if connected to the same local network. Each operator opens `web/index.html` in their browser.

---

## Log directory

Logs are written to `./logs/` relative to the working directory:

```
logs/
â”œâ”€â”€ decisions.jsonl          All evaluation results
â”œâ”€â”€ residue.jsonl            Unresolved residue records
â”œâ”€â”€ incidents.jsonl          Saved incident library entries
â”œâ”€â”€ overrides.jsonl          Simple override log
â””â”€â”€ override_records/        Formal accountability records (one JSON per record)
```

Logs are append-only JSONL files. They can be backed up, exported, or analysed independently.

To change the log directory, set the environment variable before starting the server:

```bash
export BOUNDARY_LOG_DIR=/path/to/logs
python -m uvicorn api.server:app --host 127.0.0.1 --port 8787
```

---

## Multiple instances

Each instance of the backend maintains its own log directory. For shared audit logging across multiple instances, configure all instances to write to the same directory on a shared drive.

---

## Security notes

The backend binds to `127.0.0.1` by default and is not accessible from other machines. For institutional deployment on a local network, change the host:

```bash
python -m uvicorn api.server:app --host 0.0.0.0 --port 8787
```

Consider adding authentication appropriate to your deployment context. The platform does not include authentication by default.

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `BOUNDARY_LOG_DIR` | `./logs` | Directory for all log files |

---

## Upgrading

Replace all files except the `logs/` directory. Logs are backward-compatible â€” JSONL format does not change between versions.

