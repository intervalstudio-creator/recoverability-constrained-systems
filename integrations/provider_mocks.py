from engine.audit import write_audit_record

def mock_identity_continuity(case_id: str):
    result = {"provider":"mock_identity","case_id":case_id,"actions":["preserve_access_temporarily","issue_secondary_verification","route_to_manual_review"]}
    write_audit_record("provider_mock","executed",result); return result

def mock_wallet_continuity(case_id: str):
    result = {"provider":"mock_wallet","case_id":case_id,"actions":["unlock_minimum_wallet_floor","preserve_basic_transactions","log_restricted_state"]}
    write_audit_record("provider_mock","executed",result); return result

def mock_transport_dispatch(case_id: str):
    result = {"provider":"mock_transport","case_id":case_id,"actions":["open_dispatch_escalation","request_alternate_route","preserve_care_transfer_window"]}
    write_audit_record("provider_mock","executed",result); return result

def mock_emergency_broadcast(case_id: str):
    result = {"provider":"mock_emergency","case_id":case_id,"actions":["issue_public_warning","broadcast_safe_path","activate_restriction_state"]}
    write_audit_record("provider_mock","executed",result); return result
