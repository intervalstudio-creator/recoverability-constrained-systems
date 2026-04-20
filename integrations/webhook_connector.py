import hashlib
import hmac
import json
import requests
from engine.config import get_env, get_int
from engine.retry import with_retry

def _signature(secret: str, body: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

def send_webhook(url: str, payload: dict):
    secret = get_env("BOUNDARY_SHARED_WEBHOOK_SECRET", "change_me")
    timeout = get_int("BOUNDARY_REQUEST_TIMEOUT_SECONDS", 5)
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = _signature(secret, body)

    def _send():
        r = requests.post(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-Boundary-Signature": signature,
                "X-Boundary-Event": payload.get("event", "boundary.event")
            },
            timeout=timeout
        )
        r.raise_for_status()
        return {"status_code": r.status_code, "text": r.text[:300]}

    resp = with_retry(_send, retriable_exceptions=(requests.RequestException,))
    return {"ok": True, "channel": "webhook", "response": resp}
