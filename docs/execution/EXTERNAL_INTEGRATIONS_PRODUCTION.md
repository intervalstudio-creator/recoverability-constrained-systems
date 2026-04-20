# External Integrations — Production Layer

Included channels:
- Email (SMTP)
- SMS (Twilio)
- Incident (PagerDuty)
- Webhook (signed)
- Device actuation (through signed webhook)

If providers are not configured, failed actions are captured through observability and dead-letter handling.
