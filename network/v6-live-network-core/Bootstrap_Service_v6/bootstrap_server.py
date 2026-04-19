import argparse, os, json, time
from flask import Flask, request, jsonify, render_template_string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REGISTRY_FILE = os.path.join(DATA_DIR, "registry.json")
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)
STATE = {"port": 9000, "ttl_seconds": 60}

HTML = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Continuity Bootstrap v6</title>
<style>
body{font-family:Arial;background:#0b0b0b;color:#f2f2f2;margin:0}
.wrap{max-width:1000px;margin:0 auto;padding:24px}
.card{background:#151515;border:1px solid #2b2b2b;border-radius:12px;padding:16px;margin-bottom:16px}
.msg{border-top:1px solid #2b2b2b;padding:10px 0}
.small{color:#bbb;font-size:12px}
.pill{display:inline-block;padding:4px 10px;border-radius:999px;background:#222;border:1px solid #333;margin-right:8px;margin-bottom:8px}
</style></head>
<body><div class="wrap">
<h1>Continuity Bootstrap Service v6</h1>
<div class="card">
<div class="pill">Port: {{ port }}</div>
<div class="pill">Registered Nodes: {{ count }}</div>
<div class="pill">TTL: {{ ttl }}s</div>
</div>
<div class="card">
<h2>Nodes</h2>
{% if nodes %}
{% for n in nodes %}
<div class="msg">
<div><strong>{{ n.node_name }}</strong></div>
<div class="small">{{ n.url }}</div>
<div class="small">last_seen={{ n.last_seen }}</div>
</div>
{% endfor %}
{% else %}
<p>No nodes registered.</p>
{% endif %}
</div>
</div></body></html>
"""

def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return []
    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_registry(reg):
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)

def prune_registry():
    reg = load_registry()
    now = time.time()
    reg = [n for n in reg if now - n.get("last_seen_epoch", 0) <= STATE["ttl_seconds"]]
    save_registry(reg)
    return reg

@app.route("/")
def index():
    reg = prune_registry()
    reg.sort(key=lambda x: x.get("last_seen_epoch", 0), reverse=True)
    return render_template_string(HTML, port=STATE["port"], count=len(reg), ttl=STATE["ttl_seconds"], nodes=reg)

@app.route("/api/health")
def health():
    return jsonify({"status": "ACTIVE", "service": "bootstrap", "port": STATE["port"], "timestamp": time.time()})

@app.route("/api/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True) or {}
    node_name = payload.get("node_name", "").strip()
    url = payload.get("url", "").strip().rstrip("/")
    if not node_name or not url:
        return jsonify({"ok": False, "error": "missing node_name/url"}), 400
    reg = prune_registry()
    found = False
    now = time.time()
    for n in reg:
        if n["url"] == url:
            n["node_name"] = node_name
            n["last_seen_epoch"] = now
            n["last_seen"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            found = True
            break
    if not found:
        reg.append({
            "node_name": node_name,
            "url": url,
            "last_seen_epoch": now,
            "last_seen": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        })
    save_registry(reg)
    return jsonify({"ok": True, "registered": url, "count": len(reg)})

@app.route("/api/heartbeat", methods=["POST"])
def heartbeat():
    payload = request.get_json(silent=True) or {}
    url = payload.get("url", "").strip().rstrip("/")
    reg = prune_registry()
    now = time.time()
    for n in reg:
        if n["url"] == url:
            n["last_seen_epoch"] = now
            n["last_seen"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            save_registry(reg)
            return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "node not registered"}), 404

@app.route("/api/peers")
def peers():
    reg = prune_registry()
    return jsonify({"peers": reg})

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=9000)
    p.add_argument("--ttl-seconds", type=int, default=60)
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    STATE["port"] = args.port
    STATE["ttl_seconds"] = max(15, args.ttl_seconds)
    app.run(host="0.0.0.0", port=args.port, debug=False)
