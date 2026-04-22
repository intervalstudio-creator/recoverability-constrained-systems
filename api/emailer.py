import os

import requests

SENDGRID_KEY = os.getenv("SENDGRID_KEY")
EMAIL_TO = os.getenv("ALERT_EMAIL")


def send_email(subject, body):
    if not SENDGRID_KEY or not EMAIL_TO:
        return
    requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={"Authorization": f"Bearer {SENDGRID_KEY}"},
        json={
            "personalizations": [{"to": [{"email": EMAIL_TO}]}],
            "from": {"email": "alert@recovs.system"},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}],
        },
        timeout=15,
    )
