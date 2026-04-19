# Continuity Network v6 — Bootstrap Service

This is the first live network layer for the continuity network.

## What it does
- node registration
- peer directory
- heartbeat / liveness
- network-visible bootstrap discovery
- no central messaging authority, only coordination

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python bootstrap_server.py --port 9000
```

Open:
- http://127.0.0.1:9000

## Endpoints
- `/api/register`
- `/api/heartbeat`
- `/api/peers`
- `/api/health`

## Purpose
This is not the whole production stack.
It is the first required live coordination service so nodes can discover each other beyond manual configuration.
