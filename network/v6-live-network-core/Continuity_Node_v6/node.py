import argparse, os, json, threading, time, hashlib, socket, secrets
from datetime import datetime, timezone
from flask import Flask, request, redirect, render_template, jsonify, send_file
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")
PEERS_FILE = os.path.join(DATA_DIR, "peers.json")
QUEUE_FILE = os.path.join(DATA_DIR, "relay_queue.json")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
KEY_FILE = os.path.join(DATA_DIR, "node_key.json")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

app = Flask(__name__)
STATE = {"node_name": "continuity-node", "port": 8080, "status": "ACTIVE", "bootstrap": "", "auto_sync_seconds": 12, "key_id": "unknown"}

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def ts_epoch():
    return time.time()

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, payload):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

def log_event(kind, detail):
    events = load_json(EVENTS_FILE, [])
    events.insert(0, {"timestamp": utc_now(), "kind": kind, "detail": detail})
    save_json(EVENTS_FILE, events[:300])

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def local_urls():
    local = f"http://127.0.0.1:{STATE['port']}"
    lip = get_local_ip()
    lan = f"http://{lip}:{STATE['port']}" if lip else None
    return local, lan

def get_or_create_key():
    data = load_json(KEY_FILE, None)
    if data and "secret" in data:
        return data
    secret = secrets.token_hex(32)
    key_id = hashlib.sha256(secret.encode()).hexdigest()[:12]
    data = {"secret": secret, "key_id": key_id}
    save_json(KEY_FILE, data)
    return data

def sign_message(msg, secret):
    body = "|".join([msg["author"], msg["content"], msg["priority"], ",".join(msg.get("tags", [])), msg["timestamp"], msg["node_name"], msg["id"]])
    return hashlib.sha256((body + "|" + secret).encode()).hexdigest()

def make_message(author, content, priority, tags):
    ts = utc_now()
    raw = f"{author}|{content}|{priority}|{','.join(tags)}|{ts}|{STATE['node_name']}".encode()
    mid = hashlib.sha256(raw).hexdigest()[:16]
    msg = {"author": author.strip(), "content": content.strip(), "priority": priority, "tags": tags, "timestamp": ts, "node_name": STATE["node_name"], "id": mid, "hops": 0, "acks": [], "ack_count": 0}
    key = get_or_create_key()
    msg["signature"] = sign_message(msg, key["secret"])
    return msg

def load_messages():
    return load_json(MESSAGES_FILE, [])

def save_messages(messages):
    save_json(MESSAGES_FILE, messages)

def load_peers():
    return load_json(PEERS_FILE, [])

def save_peers(peers):
    seen = {}
    local, lan = local_urls()
    for p in peers:
        url = (p.get("url") or "").strip().rstrip("/")
        if url and url not in {local, lan}:
            seen[url] = {"url": url, "status": p.get("status", "UNKNOWN"), "last_checked": p.get("last_checked")}
    save_json(PEERS_FILE, list(seen.values()))

def load_queue():
    return load_json(QUEUE_FILE, [])

def save_queue(queue):
    save_json(QUEUE_FILE, queue)

def dedupe_messages(messages):
    keep = {}
    for m in messages:
        mid = m["id"]
        m.setdefault("acks", [])
        m["ack_count"] = len(m["acks"])
        if mid not in keep:
            keep[mid] = m
        else:
            cur = keep[mid]
            cur["acks"] = sorted(set(cur.get("acks", []) + m.get("acks", [])))
            cur["ack_count"] = len(cur["acks"])
            cur["hops"] = min(cur.get("hops", 9999), m.get("hops", 9999))
            keep[mid] = cur
    return list(keep.values())

def enqueue(messages, targets):
    q = load_queue()
    now = ts_epoch()
    for m in messages:
        for t in targets:
            q.append({"message_id": m["id"], "target": t, "message": m, "attempts": 0, "next_try": now})
    save_queue(q)

def flush_queue_once():
    q = load_queue()
    now = ts_epoch()
    remaining = []
    for item in q:
        if item["next_try"] > now:
            remaining.append(item)
            continue
        try:
            r = requests.post(item["target"].rstrip("/") + "/api/ingest", json={"messages": [item["message"]]}, timeout=2)
            if r.ok:
                log_event("relay_sent", f"{item['message_id']} -> {item['target']}")
                continue
        except Exception:
            pass
        item["attempts"] += 1
        item["next_try"] = now + min(60, 2 ** min(item["attempts"], 5))
        remaining.append(item)
    save_queue(remaining)

def add_message(author, content, priority, tags):
    msgs = dedupe_messages(load_messages() + [make_message(author, content, priority, tags)])
    msgs.sort(key=lambda x: x["timestamp"], reverse=True)
    save_messages(msgs)
    enqueue([msgs[0]], [p["url"] for p in load_peers()])
    log_event("post", msgs[0]["id"])

def merge_messages(incoming):
    current = load_messages()
    current_ids = {m["id"] for m in current}
    new_items = []
    for m in incoming:
        if m["id"] not in current_ids:
            m["hops"] = int(m.get("hops", 0)) + 1
            m.setdefault("acks", [])
            m["ack_count"] = len(m["acks"])
            new_items.append(m)
    merged = dedupe_messages(current + incoming)
    merged.sort(key=lambda x: x["timestamp"], reverse=True)
    save_messages(merged)
    return new_items

def refresh_peer_status():
    peers = load_peers()
    updated = []
    for p in peers:
        status = "OFFLINE"
        checked = utc_now()
        try:
            r = requests.get(p["url"] + "/api/health", timeout=2)
            if r.ok:
                status = r.json().get("status", "ACTIVE")
        except Exception:
            status = "OFFLINE"
        updated.append({"url": p["url"], "status": status, "last_checked": checked})
    save_peers(updated)

def bootstrap_register():
    if not STATE["bootstrap"]:
        return
    local, lan = local_urls()
    url = lan or local
    try:
        requests.post(STATE["bootstrap"].rstrip("/") + "/api/register", json={"node_name": STATE["node_name"], "url": url}, timeout=2)
        log_event("bootstrap_register", url)
    except Exception:
        pass

def bootstrap_heartbeat():
    if not STATE["bootstrap"]:
        return
    local, lan = local_urls()
    url = lan or local
    try:
        requests.post(STATE["bootstrap"].rstrip("/") + "/api/heartbeat", json={"url": url}, timeout=2)
    except Exception:
        pass

def bootstrap_refresh_peers():
    if not STATE["bootstrap"]:
        return []
    local, lan = local_urls()
    me = {local}
    if lan:
        me.add(lan)
    try:
        r = requests.get(STATE["bootstrap"].rstrip("/") + "/api/peers", timeout=2)
        if r.ok:
            peers = load_peers()
            for item in r.json().get("peers", []):
                url = item["url"].rstrip("/")
                if url not in me:
                    peers.append({"url": url, "status": "UNKNOWN", "last_checked": None})
            save_peers(peers)
            return peers
    except Exception:
        pass
    return []

def sync_once():
    bootstrap_refresh_peers()
    peers = load_peers()
    new_for_queue = []
    for p in peers:
        try:
            r = requests.get(p["url"] + "/api/messages", timeout=3)
            if r.ok:
                new_items = merge_messages(r.json().get("messages", []))
                if new_items:
                    new_for_queue.extend(new_items)
                    log_event("sync", f"{len(new_items)} from {p['url']}")
        except Exception:
            pass
    if new_for_queue:
        enqueue(new_for_queue, [p["url"] for p in peers])
    refresh_peer_status()

def export_state():
    return {"node_name": STATE["node_name"], "port": STATE["port"], "bootstrap": STATE["bootstrap"], "messages": load_messages(), "peers": load_peers(), "relay_queue": load_queue(), "events": load_json(EVENTS_FILE, [])}

def import_state(payload):
    msgs = dedupe_messages(load_messages() + payload.get("messages", []))
    msgs.sort(key=lambda x: x["timestamp"], reverse=True)
    save_messages(msgs)
    save_peers(load_peers() + payload.get("peers", []))
    save_queue(load_queue() + payload.get("relay_queue", []))
    log_event("import", f"messages={len(payload.get('messages', []))}")

def create_backup():
    path = os.path.join(BACKUP_DIR, f"backup_{int(time.time())}.json")
    save_json(path, export_state())
    log_event("backup", os.path.basename(path))
    return path

def ack_message(mid):
    msgs = load_messages()
    changed = False
    for m in msgs:
        if m["id"] == mid and STATE["node_name"] not in m.get("acks", []):
            m.setdefault("acks", []).append(STATE["node_name"])
            m["ack_count"] = len(m["acks"])
            changed = True
    if changed:
        save_messages(msgs)
        enqueue([m for m in msgs if m["id"] == mid], [p["url"] for p in load_peers()])
        log_event("ack", mid)

def worker():
    while True:
        try:
            bootstrap_register()
            bootstrap_heartbeat()
            sync_once()
            flush_queue_once()
        except Exception:
            pass
        time.sleep(STATE["auto_sync_seconds"])

@app.route("/")
def index():
    msgs = load_messages()
    peers = load_peers()
    local, lan = local_urls()
    return render_template("index.html", node_name=STATE["node_name"], port=STATE["port"], status=STATE["status"],
                           bootstrap=STATE["bootstrap"], peer_count=len(peers), message_count=len(msgs), queue_count=len(load_queue()),
                           peers=peers, messages=msgs, events=load_json(EVENTS_FILE, []), local_url=local, local_ip_url=lan)

@app.route("/post", methods=["POST"])
def post():
    author = request.form.get("author","").strip()
    content = request.form.get("content","").strip()
    priority = request.form.get("priority","normal").strip()
    tags = [t.strip() for t in request.form.get("tags","").split(",") if t.strip()]
    if author and content:
        add_message(author, content, priority, tags)
    return redirect("/")

@app.route("/sync", methods=["POST"])
def sync_route():
    sync_once()
    return redirect("/")

@app.route("/bootstrap_refresh", methods=["POST"])
def boot_refresh():
    bootstrap_refresh_peers()
    return redirect("/")

@app.route("/flush_queue", methods=["POST"])
def flush_route():
    flush_queue_once()
    return redirect("/")

@app.route("/backup", methods=["POST"])
def backup_route():
    create_backup()
    return redirect("/")

@app.route("/add_peer", methods=["POST"])
def add_peer():
    url = request.form.get("peer_url","").strip().rstrip("/")
    if url:
        peers = load_peers()
        peers.append({"url": url, "status": "UNKNOWN", "last_checked": None})
        save_peers(peers)
        log_event("peer_add", url)
    return redirect("/")

@app.route("/remove_peer", methods=["POST"])
def remove_peer():
    url = request.form.get("peer_url","").strip().rstrip("/")
    save_peers([p for p in load_peers() if p["url"] != url])
    log_event("peer_remove", url)
    return redirect("/")

@app.route("/ack", methods=["POST"])
def ack():
    mid = request.form.get("message_id","").strip()
    if mid:
        ack_message(mid)
    return redirect("/")

@app.route("/export")
def export_route():
    path = os.path.join(DATA_DIR, "export_state.json")
    save_json(path, export_state())
    return send_file(path, as_attachment=True, download_name="continuity_node_v6_export.json")

@app.route("/import", methods=["POST"])
def import_route():
    f = request.files.get("import_file")
    if f:
        payload = json.load(f.stream)
        import_state(payload)
    return redirect("/")

@app.route("/api/health")
def api_health():
    return jsonify({"status": STATE["status"], "node_name": STATE["node_name"], "port": STATE["port"], "timestamp": time.time()})

@app.route("/api/messages")
def api_messages():
    return jsonify({"node_name": STATE["node_name"], "messages": load_messages()})

@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    incoming = (request.get_json(silent=True) or {}).get("messages", [])
    new_items = merge_messages(incoming)
    if new_items:
        enqueue(new_items, [p["url"] for p in load_peers()])
        log_event("ingest", f"accepted {len(new_items)}")
    return jsonify({"accepted": len(new_items)})

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--name", type=str, default="continuity-node")
    p.add_argument("--bootstrap", type=str, default="")
    p.add_argument("--auto-sync-seconds", type=int, default=12)
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    STATE["port"] = args.port
    STATE["node_name"] = args.name
    STATE["bootstrap"] = args.bootstrap.strip().rstrip("/")
    STATE["auto_sync_seconds"] = max(5, args.auto_sync_seconds)
    STATE["key_id"] = get_or_create_key()["key_id"]
    for path, default in [(MESSAGES_FILE, []),(PEERS_FILE, []),(QUEUE_FILE, []),(EVENTS_FILE, [])]:
        if not os.path.exists(path):
            save_json(path, default)
    threading.Thread(target=worker, daemon=True).start()
    app.run(host="0.0.0.0", port=args.port, debug=False)
