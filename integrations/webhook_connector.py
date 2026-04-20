import hashlib, hmac, json, requests
from engine.config import get_env, get_int
from engine.retry import with_retry

def sign_body(body: bytes) -> str:
    secret = get_env("BOUNDARY_SHARED_WEBHOOK_SECRET", "change_me")
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

def send_webhook(url: str, payload: dict):
    if not url:
        raise RuntimeError("Webhook endpoint not configured")
    timeout = get_int("BOUNDARY_REQUEST_TIMEOUT_SECONDS", 5)
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    signature = sign_body(body)
    def _send():
        r = requests.post(url, data=body, headers={"Content-Type":"application/json","X-Boundary-Signature":signature}, timeout=timeout)
        r.raise_for_status()
        return {"status_code": r.status_code, "text": r.text[:200]}
    return {"ok": True, "channel": "webhook", "response": with_retry(_send, retriable_exceptions=(requests.RequestException,))}
