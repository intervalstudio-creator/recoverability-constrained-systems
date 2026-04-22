# Boundary v4.1 Patch Instructions

## What this patch changes
This patch keeps Boundary as an evaluation and escalation platform.
It adds an optional forwarding layer to the external enforcement module.

## File placement
Copy these files into the matching folders in your project:

- `web/app.js` -> `web/` (integrate equivalent connector logic into the current RECOVS UI)
- `engine/enforcement_client.py` -> `engine/`
- `api/enforcement_routes_patch.py` -> `api/`
- `config/enforcement_integration.json` -> `config/`
- this file -> `docs/` or keep externally

---

## Option A â€” UI patch (current RECOVS surface)

Use this when the final result is produced in `web/index.html`.

### 1. Load the connector script
Add near the end of `web/index.html`:

```html
<script src="./app.js"></script>
```

### 2. Enable when you want forwarding
For testing:

```html
<script>
  window.BoundaryEnforcement.setEnabled(true);
  window.BoundaryEnforcement.setEndpoint("http://127.0.0.1:8010/evaluate");
</script>
```

### 3. Forward after result rendering
Add:

```html
<script>
async function forwardBoundaryResult(result, domain) {
  const response = await window.BoundaryEnforcement.send(result, {
    domain: domain || result.domain || "unknown",
    evaluation_id: result.evaluation_id || `BND-${Date.now()}`,
    timestamp: result.timestamp || new Date().toISOString()
  });
  console.log("Boundary enforcement forward status:", response);
}
</script>
```

Then call:

```javascript
forwardBoundaryResult(result, selectedDomain);
```

right after your platform computes the final evaluation output.

---

## Option B â€” API patch

Use this when the backend route is the main source of evaluation results.

### 1. Import helper
Inside your API route file:

```python
from engine.enforcement_client import maybe_forward_to_enforcement
```

### 2. Call it after evaluation
```python
forward_status = maybe_forward_to_enforcement(
    result,
    context={
        "evaluation_id": result.get("evaluation_id"),
        "timestamp": result.get("timestamp"),
        "domain": result.get("domain")
    }
)
```

### 3. Return it together
```python
return {
    "result": result,
    "enforcement": forward_status
}
```

---

## Default safe mode
Keep this in `config/enforcement_integration.json`:

```json
"enabled": false
```

Switch to true only when:
- the enforcement module is running
- you want forwarding enabled
- you have tested one case successfully

---

## Recommended order
1. Copy files into your project
2. Keep forwarding disabled
3. Start the external enforcement module
4. Enable forwarding
5. Test with one NON-ADMISSIBLE case

