window.BoundaryEnforcement = (() => {
  const config = {
    enabled: false,
    endpoint: "http://127.0.0.1:8010/evaluate",
    forwardStates: ["DEGRADED", "NON-ADMISSIBLE", "NON-EXECUTABLE"],
    failOpen: true
  };

  function normalizeState(state) {
    if (!state) return "UNKNOWN";
    const s = String(state).trim().toUpperCase();
    if (s === "STOP") return "NON-ADMISSIBLE";
    if (s === "HALT") return "NON-EXECUTABLE";
    return s;
  }

  function buildPayload(result, context = {}) {
    const state = normalizeState(result.state || result.admissibility_state || result.decision);
    return {
      evaluation_id: context.evaluation_id || result.evaluation_id || `BND-${Date.now()}`,
      timestamp: context.timestamp || result.timestamp || new Date().toISOString(),
      domain: context.domain || result.domain || "unknown",
      state,
      reason_codes: result.reason_codes || result.failed_rules || [],
      summary: result.summary || result.explanation || result.plain_language || "Boundary evaluation result forwarded to enforcement layer.",
      source: "boundary-v4.1",
      raw_result: result
    };
  }

  async function send(result, context = {}) {
    const payload = buildPayload(result, context);
    if (!config.enabled) {
      return { ok: true, skipped: true, reason: "enforcement_disabled", payload };
    }
    if (!config.forwardStates.includes(payload.state)) {
      return { ok: true, skipped: true, reason: "state_not_forwarded", payload };
    }

    try {
      const res = await fetch(config.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      return { ok: true, forwarded: true, payload, response: data };
    } catch (err) {
      if (config.failOpen) {
        return { ok: true, forwarded: false, fail_open: true, error: String(err), payload };
      }
      return { ok: false, forwarded: false, error: String(err), payload };
    }
  }

  function setEnabled(v) { config.enabled = !!v; }
  function setEndpoint(v) { config.endpoint = String(v); }
  function setForwardStates(v) { config.forwardStates = Array.isArray(v) ? v : config.forwardStates; }

  return {
    config,
    normalizeState,
    buildPayload,
    send,
    setEnabled,
    setEndpoint,
    setForwardStates
  };
})();
