import requests
from engine.config import get_env
from engine.retry import with_retry

def send_sms(number: str, message: str):
    sid = get_env("BOUNDARY_TWILIO_ACCOUNT_SID")
    token = get_env("BOUNDARY_TWILIO_AUTH_TOKEN")
    sender = get_env("BOUNDARY_TWILIO_FROM")
    if not sid or not token or not sender:
        raise RuntimeError("SMS provider not configured")

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"

    def _send():
        r = requests.post(
            url,
            auth=(sid, token),
            data={"To": number, "From": sender, "Body": message},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    resp = with_retry(_send, retriable_exceptions=(requests.RequestException,))
    return {"ok": True, "channel": "sms", "to": number, "provider_response": resp}
