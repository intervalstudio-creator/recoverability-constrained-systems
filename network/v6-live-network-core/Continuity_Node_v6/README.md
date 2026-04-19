# Continuity Node v6

Distributed execution node operating under recoverability constraints.

Each node evaluates, propagates, and enforces admissible continuation in real time.

---

## Purpose

- run local execution environment  
- exchange messages with peers  
- synchronize state across network  
- enforce continuation boundary  

---

## Core Principle

A system may act only while recoverability can be established in time under real conditions.

If this cannot be established:

→ continuation is non-admissible  
→ execution does not occur  

---

## Capabilities

- local-first operation  
- peer discovery via bootstrap  
- message propagation  
- relay queue and retry logic  
- state synchronization  
- independent enforcement  

---

## Key Files

- `node.py` — main node service  
- `data/messages.json` — local messages  
- `data/peers.json` — known peers  
- `data/relay_queue.json` — pending propagation  
- `requirements.txt` — dependencies  

---

## Run

```bash
pip install -r requirements.txt
python node.py --port 8080 --name node-1 --bootstrap http://127.0.0.1:9000

Run additional nodes:
python node.py --port 8081 --name node-2 --bootstrap http://127.0.0.1:9000

Interface

Open in browser:

http://127.0.0.1:8080

Behavior
Nodes register with bootstrap
Discover peers dynamically
Exchange and propagate messages
Maintain local and shared state

If network is unavailable:

→ node continues locally
→ synchronization resumes when connectivity returns

Role in System

There is no central controller.

Each node independently enforces the same boundary condition.

The network extends coordination.

It does not override admissibility.

