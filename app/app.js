const API = "http://127.0.0.1:8787";
function buildEvent() {
  return {
    domain: document.getElementById("domain").value,
    event_type: document.getElementById("event_type").value,
    boundary_detectable: document.getElementById("boundary_detectable").checked,
    response_possible_in_time: document.getElementById("response_possible_in_time").checked,
    recovery_path_verified: document.getElementById("recovery_path_verified").checked,
    critical_unknowns_present: document.getElementById("critical_unknowns_present").checked,
    dependency_unavailable: document.getElementById("dependency_unavailable").checked,
    incident_title: "Boundary autonomous event",
    incident_description: "Autonomous execution decision"
  };
}
async function refreshStatus() {
  const runtime = await fetch(API + "/api/runtime-status").then(r => r.json());
  const observability = await fetch(API + "/api/observability").then(r => r.json());
  const auto = await fetch(API + "/api/auto/status").then(r => r.json());
  document.getElementById("autoState").textContent = "Auto: " + (auto.running ? "ON" : "OFF") + " | last run: " + (auto.last_run_utc || "never");
  document.getElementById("status").textContent = JSON.stringify({runtime, observability, auto}, null, 2);
}
function loadCase(domain) {
  document.getElementById("domain").value = domain;
  if (domain === "healthcare") { document.getElementById("event_type").value = "transport_failure"; document.getElementById("boundary_detectable").checked = true; document.getElementById("response_possible_in_time").checked = false; document.getElementById("recovery_path_verified").checked = false; document.getElementById("critical_unknowns_present").checked = true; document.getElementById("dependency_unavailable").checked = true; }
  else if (domain === "identity") { document.getElementById("event_type").value = "identity_breach"; document.getElementById("boundary_detectable").checked = true; document.getElementById("response_possible_in_time").checked = false; document.getElementById("recovery_path_verified").checked = false; document.getElementById("critical_unknowns_present").checked = true; document.getElementById("dependency_unavailable").checked = true; }
  else if (domain === "finance") { document.getElementById("event_type").value = "wallet_lockout"; document.getElementById("boundary_detectable").checked = true; document.getElementById("response_possible_in_time").checked = false; document.getElementById("recovery_path_verified").checked = false; document.getElementById("critical_unknowns_present").checked = true; document.getElementById("dependency_unavailable").checked = true; }
  else if (domain === "disaster") { document.getElementById("event_type").value = "tsunami_warning"; document.getElementById("boundary_detectable").checked = true; document.getElementById("response_possible_in_time").checked = false; document.getElementById("recovery_path_verified").checked = false; document.getElementById("critical_unknowns_present").checked = false; document.getElementById("dependency_unavailable").checked = true; }
}
async function submitEvent() {
  const result = await fetch(API + "/api/events", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(buildEvent())}).then(r => r.json());
  document.getElementById("decision").textContent = JSON.stringify(result, null, 2);
  refreshStatus();
}
async function startAuto() {
  const interval_seconds = parseInt(document.getElementById("autoInterval").value, 10);
  await fetch(API + "/api/auto/start", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({interval_seconds})});
  refreshStatus();
}
async function stopAuto() {
  await fetch(API + "/api/auto/stop", {method:"POST"});
  refreshStatus();
}
refreshStatus();
