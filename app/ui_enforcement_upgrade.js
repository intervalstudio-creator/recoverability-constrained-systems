(function(){
  function ensurePanel(){
    if (document.getElementById("boundary-enforcement-panel")) return;

    const panel = document.createElement("section");
    panel.id = "boundary-enforcement-panel";
    panel.className = "boundary-enforcement-panel";
    panel.innerHTML = `
      <div class="boundary-enforcement-title">Enforcement forwarding</div>

      <div class="boundary-enforcement-grid">
        <div class="boundary-enforcement-box">
          <div class="boundary-enforcement-label">Mode</div>
          <div class="boundary-enforcement-value" id="be-mode">Disabled</div>
        </div>
        <div class="boundary-enforcement-box">
          <div class="boundary-enforcement-label">Last state forwarded</div>
          <div class="boundary-enforcement-value" id="be-last-state">—</div>
        </div>
        <div class="boundary-enforcement-box">
          <div class="boundary-enforcement-label">Forwarding status</div>
          <div class="boundary-enforcement-value" id="be-last-status"><span class="boundary-pill warn">Not sent</span></div>
        </div>
        <div class="boundary-enforcement-box">
          <div class="boundary-enforcement-label">Endpoint</div>
          <div class="boundary-enforcement-value" id="be-endpoint-label">http://127.0.0.1:8010/evaluate</div>
        </div>
      </div>

      <div class="boundary-controls-row">
        <button class="boundary-btn" id="be-enable-btn" type="button">Enable forwarding</button>
        <button class="boundary-btn" id="be-disable-btn" type="button">Disable forwarding</button>
        <button class="boundary-btn" id="be-test-btn" type="button">Send test payload</button>
      </div>

      <div class="boundary-controls-row">
        <label class="boundary-field">
          <span>Endpoint</span>
          <input id="be-endpoint-input" type="text" value="http://127.0.0.1:8010/evaluate" />
        </label>
      </div>

      <pre class="boundary-pre" id="be-response-box">No forwarding response yet.</pre>
    `;

    const anchor =
      document.querySelector("#result-panel") ||
      document.querySelector("#results") ||
      document.querySelector("#output") ||
      document.querySelector("main") ||
      document.body;

    anchor.appendChild(panel);

    bindPanelEvents();
    syncPanelFromConfig();
  }

  function setHtml(id, html){
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
  }

  function setText(id, text){
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function syncPanelFromConfig(){
    if (!window.BoundaryEnforcement) return;
    const cfg = window.BoundaryEnforcement.config;
    setText("be-mode", cfg.enabled ? "Enabled" : "Disabled");
    setText("be-endpoint-label", cfg.endpoint || "—");
    const input = document.getElementById("be-endpoint-input");
    if (input) input.value = cfg.endpoint || "";
  }

  function bindPanelEvents(){
    const enableBtn = document.getElementById("be-enable-btn");
    const disableBtn = document.getElementById("be-disable-btn");
    const testBtn = document.getElementById("be-test-btn");
    const endpointInput = document.getElementById("be-endpoint-input");

    if (enableBtn) enableBtn.onclick = function(){
      window.BoundaryEnforcement.setEnabled(true);
      if (endpointInput && endpointInput.value) {
        window.BoundaryEnforcement.setEndpoint(endpointInput.value);
      }
      syncPanelFromConfig();
      setHtml("be-last-status", '<span class="boundary-pill ok">Enabled</span>');
    };

    if (disableBtn) disableBtn.onclick = function(){
      window.BoundaryEnforcement.setEnabled(false);
      syncPanelFromConfig();
      setHtml("be-last-status", '<span class="boundary-pill warn">Disabled</span>');
    };

    if (testBtn) testBtn.onclick = async function(){
      if (endpointInput && endpointInput.value) {
        window.BoundaryEnforcement.setEndpoint(endpointInput.value);
      }
      const fake = {
        evaluation_id: `BND-TEST-${Date.now()}`,
        timestamp: new Date().toISOString(),
        domain: "test",
        state: "NON-ADMISSIBLE",
        reason_codes: ["TEST"],
        summary: "UI forwarding test."
      };
      const response = await window.BoundaryEnforcement.send(fake, { domain: "test" });
      renderEnforcementForwardResult(response, fake.state);
    };
  }

  window.renderEnforcementForwardResult = function(response, state){
    setText("be-last-state", state || response?.payload?.state || "—");

    if (response?.forwarded) {
      setHtml("be-last-status", '<span class="boundary-pill ok">Forwarded</span>');
    } else if (response?.skipped) {
      setHtml("be-last-status", '<span class="boundary-pill warn">Skipped</span>');
    } else if (response?.fail_open || response?.ok) {
      setHtml("be-last-status", '<span class="boundary-pill warn">Fail-open / not forwarded</span>');
    } else {
      setHtml("be-last-status", '<span class="boundary-pill err">Error</span>');
    }

    const box = document.getElementById("be-response-box");
    if (box) {
      box.textContent = JSON.stringify(response, null, 2);
    }
  };

  window.forwardBoundaryResultWithUI = async function(result, domain){
    if (!window.BoundaryEnforcement) return null;
    const response = await window.BoundaryEnforcement.send(result, {
      domain: domain || result.domain || "unknown",
      evaluation_id: result.evaluation_id || `BND-${Date.now()}`,
      timestamp: result.timestamp || new Date().toISOString()
    });
    renderEnforcementForwardResult(response, result.state || result.admissibility_state || result.decision);
    return response;
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensurePanel);
  } else {
    ensurePanel();
  }
})();
