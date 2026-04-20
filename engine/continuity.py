def get_continuity_floor(domain: str):
    if domain == "healthcare":
        return {"minimums": ["contactable_path", "transport_path", "care_handoff", "escalation_path"]}
    if domain == "identity":
        return {"minimums": ["challenge_path", "reentry_path", "manual_review"]}
    if domain == "finance":
        return {"minimums": ["basic_wallet_access", "transaction_floor", "manual_override"]}
    return {"minimums": ["reachable_contact", "bounded_escalation_path", "fallback_path"]}
