# Continuity Node v6 — Bootstrap-Aware Network Node

This node upgrades the previous node packages by connecting to a live bootstrap service.

## Added in v6
- bootstrap registration
- live peer discovery through bootstrap
- heartbeat to bootstrap
- peer sync through discovered nodes
- local-first messaging and relay queue
- export/import/backup
- acknowledgments
- event log

## Install
```bash
pip install -r requirements.txt
```

## Start bootstrap first
```bash
python bootstrap_server.py --port 9000
```

## Run node
```bash
python node.py --port 8080 --name node-1 --bootstrap http://127.0.0.1:9000
```

## Run more nodes
```bash
python node.py --port 8081 --name node-2 --bootstrap http://127.0.0.1:9000
python node.py --port 8082 --name node-3 --bootstrap http://127.0.0.1:9000
```

Open:
- http://127.0.0.1:8080
- http://127.0.0.1:8081
- http://127.0.0.1:8082

## Fast local test
1. Start bootstrap
2. Start 2 or 3 nodes
3. Post on node 1
4. Click Sync Now on the others

## Rule
If you cannot detect, act, and recover in time → stop.
