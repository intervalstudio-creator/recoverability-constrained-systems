const API = "http://127.0.0.1:8787";

async function refreshStatus() {
  const runtime = await fetch(API + "/api/runtime-status").then(r => r.json());
  const observability = await fetch(API + "/api/observability").then(r => r.json());
  document.getElementById("status").textContent = JSON.stringify({runtime, observability}, null, 2);
}

async function setMode(mode) {
  await fetch(API + "/api/runtime/modes", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({mode})
  });
  refreshStatus();
}

function loadCase(domain) {
  document.getElementById("domain").value = domain;
  document.getElementById("boundary_detectable").checked = true;
  document.getElementById("response_possible_in_time").checked = false;
  document.getElementById("recovery_path_verified").checked = false;
  document.getElementById("critical_unknowns_present").checked = true;
  document.getElementById("dependency_unavailable").checked = true;
}

async function runCycle() {
  const payload = {
    case: {
      domain: document.getElementById("domain").value,
      boundary_detectable: document.getElementById("boundary_detectable").checked,
      response_possible_in_time: document.getElementById("response_possible_in_time").checked,
      recovery_path_verified: document.getElementById("recovery_path_verified").checked,
      critical_unknowns_present: document.getElementById("critical_unknowns_present").checked,
      dependency_unavailable: document.getElementById("dependency_unavailable").checked
    },
    actuation: {
      email: "",
      phone: "",
      incident_title: "Boundary runtime event",
      incident_description: "Automatic runtime decision"
    }
  };

  const result = await fetch(API + "/api/runtime/cycle", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  }).then(r => r.json());

  document.getElementById("decision").textContent = JSON.stringify(result, null, 2);
  refreshStatus();
}

refreshStatus();
