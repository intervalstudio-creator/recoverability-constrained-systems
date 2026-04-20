import smtplib
from email.message import EmailMessage
from engine.config import get_env, get_int
from engine.retry import with_retry

def send_email(to: str, subject: str, body: str):
    host = get_env("BOUNDARY_SMTP_HOST")
    username = get_env("BOUNDARY_SMTP_USERNAME")
    password = get_env("BOUNDARY_SMTP_PASSWORD")
    sender = get_env("BOUNDARY_EMAIL_FROM", "boundary@example.com")
    if not host or not username or not password or not to:
        raise RuntimeError("Email provider not configured")
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    def _send():
        with smtplib.SMTP(host, get_int("BOUNDARY_SMTP_PORT", 587), timeout=10) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
    with_retry(_send, retriable_exceptions=(smtplib.SMTPException, OSError))
    return {"ok": True, "channel": "email", "to": to}
