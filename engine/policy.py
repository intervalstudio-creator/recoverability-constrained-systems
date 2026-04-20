DEFAULT_POLICY = {
    "HALT": ["email", "sms", "incident", "webhook", "device"],
    "ESCALATE": ["email", "incident", "webhook"],
    "RESTRICT": ["email", "webhook"],
    "CONTAIN": ["email", "incident", "webhook"],
    "CONTINUE": []
}
def get_channels_for_decision(decision: str):
    return DEFAULT_POLICY.get(decision, [])
