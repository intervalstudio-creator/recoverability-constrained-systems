def route_authority(decision: str):
    if decision == "CONTINUE":
        return []
    return [
        {"level": 1, "role": "operator", "deadline_seconds": 60},
        {"level": 2, "role": "supervisor", "deadline_seconds": 180},
        {"level": 3, "role": "external_authority", "deadline_seconds": 600}
    ]
