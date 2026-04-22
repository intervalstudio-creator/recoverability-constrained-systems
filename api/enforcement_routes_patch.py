"""
Boundary v4.1 route patch helper.

Add this import inside your existing API server route file:
from engine.enforcement_client import maybe_forward_to_enforcement

After computing `result`, add:

forward_status = maybe_forward_to_enforcement(
    result,
    context={
        "evaluation_id": result.get("evaluation_id"),
        "timestamp": result.get("timestamp"),
        "domain": result.get("domain")
    }
)

Then return:

return {
    "result": result,
    "enforcement": forward_status
}
"""
