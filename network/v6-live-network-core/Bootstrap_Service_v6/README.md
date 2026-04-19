# Bootstrap Service v6

Entry point for the distributed network layer.

This service enables nodes to discover each other and form a coordinated network.

---

## Purpose

- register active nodes  
- maintain a live registry  
- provide peer discovery  
- enable network formation  

---

## How it works

1. A node starts and connects to the bootstrap service  
2. The node registers its address  
3. The bootstrap stores it in the registry  
4. Other nodes query the registry to discover peers  

---

## Key Files

- `bootstrap_server.py` — main service  
- `registry.json` — active nodes  
- `requirements.txt` — dependencies  

---

## Run

```bash
pip install -r requirements.txt
python bootstrap_server.py --port 9000

Windows:
run_bootstrap_windows.bat
