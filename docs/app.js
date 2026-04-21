const SITUATIONS = [
  {
    id: "pharmacological",
    icon: "💊",
    label: "Medication problem",
    sub: "Prescription / supply",
    authority: "Prescriber, pharmacist, urgent care, emergency service",
    questions: [
      { id:"q1", text:"Do you have enough medication to last the next few days?", sub:"Include pills, patches, injections, or other forms.", yn:true, field:"supply_days_remaining", yes:7, no:0 },
      { id:"q2", text:"Can you reach your doctor or prescriber right now?", sub:"By phone, online, or in person.", yn:true, field:"prescriber_reachable", yes:true, no:false },
      { id:"q3", text:"Would stopping this medication suddenly be dangerous?", sub:"Examples: benzodiazepines, insulin, epilepsy or heart medication.", yn:true, field:"abrupt_stop_risk", yes:true, no:false },
      { id:"q4", text:"Can you get to a pharmacy or have medication delivered?", yn:true, field:"dispensing_accessible", yes:true, no:false },
      { id:"q5", text:"Is there any backup option — urgent clinic, emergency prescription, out-of-hours doctor?", yn:true, field:"fallback_path_available", yes:true, no:false },
      { id:"q6", text:"Is there someone who can actually help right now?", yn:true, field:"human_authority_reachable", yes:true, no:false },
      { id:"q7", text:"How many hours before this becomes a serious emergency if nothing changes?", num:true, field:"time_remaining_seconds", unit:"hours", mult:3600 }
    ]
  },
  {
    id: "healthcare",
    icon: "🏥",
    label: "Healthcare problem",
    sub: "Appointment / care / hospital",
    authority: "Hospital, responsible clinician, emergency service",
    questions: [
      { id:"q1", text:"Have you missed or are you about to miss a critical medical appointment?", yn:true, field:"critical_appointment_missed", yes:true, no:false },
      { id:"q2", text:"Do you have a way to get to the hospital or clinic if needed?", yn:true, field:"transport_available", yes:true, no:false },
      { id:"q3", text:"Is your carer or support person available right now?", yn:true, field:"caregiver_available", yes:true, no:false },
      { id:"q4", text:"Can you reach a doctor, nurse, or emergency service right now?", yn:true, field:"human_authority_reachable", yes:true, no:false },
      { id:"q5", text:"Is there an alternative — different hospital, home visit, urgent helpline?", yn:true, field:"fallback_path_available", yes:true, no:false },
      { id:"q6", text:"How many hours before this becomes a serious emergency?", num:true, field:"time_remaining_seconds", unit:"hours", mult:3600 }
    ]
  },
  {
    id: "finance",
    icon: "💳",
    label: "Money / bank problem",
    sub: "Account / payment / benefits",
    authority: "Bank, welfare service, housing authority, emergency support service",
    questions: [
      { id:"q1", text:"Is your bank account locked or frozen?", yn:true, field:"bank_locked", yes:true, no:false },
      { id:"q2", text:"Are you unable to pay for something essential — rent, food, medication, utilities?", yn:true, field:"essential_payment_blocked", yes:true, no:false },
      { id:"q3", text:"Has your income, wages, or benefits stopped or been delayed?", yn:true, field:"income_interrupted", yes:true, no:false },
      { id:"q4", text:"Can you reach your bank, welfare service, or someone who can help right now?", yn:true, field:"human_authority_reachable", yes:true, no:false },
      { id:"q5", text:"Is there any alternative — different account, family help, crisis fund?", yn:true, field:"fallback_path_available", yes:true, no:false },
      { id:"q6", text:"How many hours before you face a serious consequence?", num:true, field:"time_remaining_seconds", unit:"hours", mult:3600 }
    ]
  },
  {
    id: "housing",
    icon: "🏠",
    label: "Housing problem",
    sub: "Eviction / shelter / utilities",
    authority: "Housing office, council, emergency accommodation service",
    questions: [
      { id:"q1", text:"Are you facing eviction or being forced to leave your home?", yn:true, field:"eviction_imminent", yes:true, no:false },
      { id:"q2", text:"Have your gas, electricity, or water been cut off?", yn:true, field:"utilities_disconnected", yes:true, no:false },
      { id:"q3", text:"Is your home currently unsafe or uninhabitable?", yn:true, field:"habitability_failure", yes:true, no:false },
      { id:"q4", text:"Can you reach a housing officer or emergency housing service right now?", yn:true, field:"human_authority_reachable", yes:true, no:false },
      { id:"q5", text:"Is there anywhere else you could go — family, shelter, emergency accommodation?", yn:true, field:"fallback_path_available", yes:true, no:false },
      { id:"q6", text:"How many hours before this becomes a crisis?", num:true, field:"time_remaining_seconds", unit:"hours", mult:3600 }
    ]
  },
  {
    id: "identity",
    icon: "🪪",
    label: "Identity / documents",
    sub: "Lost ID / locked out of services",
    authority: "Identity office, employer, bank, service provider",
    questions: [
      { id:"q1", text:"Have you lost your identity documents — passport, licence, or ID card?", yn:true, field:"id_document_available", yes:false, no:true },
      { id:"q2", text:"Are you locked out of essential accounts or services because of missing ID?", yn:true, field:"access_recovery_available", yes:false, no:true },
      { id:"q3", text:"Is your ability to receive wages or benefits affected?", yn:true, field:"payroll_identity_intact", yes:false, no:true },
      { id:"q4", text:"Can you reach a government office, employer, or recovery service right now?", yn:true, field:"human_authority_reachable", yes:true, no:false },
      { id:"q5", text:"Is there any alternative way to prove identity for now?", yn:true, field:"fallback_path_available", yes:true, no:false },
      { id:"q6", text:"How many hours before this causes a serious problem?", num:true, field:"time_remaining_seconds", unit:"hours", mult:3600 }
    ]
  },
  {
    id: "disaster",
    icon: "⚠️",
    label: "Emergency / disaster",
    sub: "Evacuation / safety / crisis",
    authority: "Emergency service, shelter authority, crisis support",
    questions: [
      { id:"q1", text:"Is there still time to reach safety or evacuate?", yn:true, field:"evacuation_window_closed", yes:false, no:true },
      { id:"q2", text:"Have you been directed to a shelter or safe location?", yn:true, field:"shelter_assigned", yes:true, no:false },
      { id:"q3", text:"Have you lost the ability to communicate with emergency services or family?", yn:true, field:"comms_collapsed", yes:true, no:false },
      { id:"q4", text:"Can you reach emergency services or someone who can help right now?", yn:true, field:"human_authority_reachable", yes:true, no:false },
      { id:"q5", text:"Is there a route or plan that still leads to safety?", yn:true, field:"fallback_path_available", yes:true, no:false },
      { id:"q6", text:"How many hours before the situation becomes irreversible?", num:true, field:"time_remaining_seconds", unit:"hours", mult:3600 }
    ]
  }
];

const DOMAIN_RULES = {
  pharmacological:[
    {id:"PH-001",field:"supply_days_remaining",min:1,weight:"critical",plain:"Medication supply has run out or will run out imminently"},
    {id:"PH-002",field:"prescriber_reachable",val:true,weight:"critical",plain:"You cannot reach your prescriber"},
    {id:"PH-003",field:"abrupt_stop_risk",val:false,weight:"critical",plain:"Stopping this medication suddenly is dangerous"},
    {id:"PH-004",field:"dispensing_accessible",val:true,weight:"major",plain:"You cannot access a pharmacy or delivery"}
  ],
  healthcare:[
    {id:"HC-001",field:"critical_appointment_missed",val:false,weight:"critical",plain:"A critical appointment has been or will be missed"},
    {id:"HC-002",field:"transport_available",val:true,weight:"major",plain:"You have no way to get to hospital or clinic"},
    {id:"HC-003",field:"caregiver_available",val:true,weight:"critical",plain:"Your carer or support person is not available"}
  ],
  finance:[
    {id:"FI-001",field:"bank_locked",val:false,weight:"critical",plain:"Your bank account is locked or frozen"},
    {id:"FI-002",field:"essential_payment_blocked",val:false,weight:"critical",plain:"You cannot pay for essential needs"},
    {id:"FI-003",field:"income_interrupted",val:false,weight:"major",plain:"Income or benefits have stopped or been delayed"}
  ],
  housing:[
    {id:"HO-001",field:"eviction_imminent",val:false,weight:"critical",plain:"You are facing imminent eviction"},
    {id:"HO-002",field:"utilities_disconnected",val:false,weight:"major",plain:"Utilities have been cut off"},
    {id:"HO-003",field:"habitability_failure",val:false,weight:"critical",plain:"Your home is unsafe or uninhabitable"}
  ],
  identity:[
    {id:"ID-001",field:"id_document_available",val:true,weight:"major",plain:"Identity documents are not available"},
    {id:"ID-002",field:"access_recovery_available",val:true,weight:"major",plain:"You are locked out of essential services due to missing ID"},
    {id:"ID-003",field:"payroll_identity_intact",val:true,weight:"major",plain:"Ability to receive wages or benefits is affected"}
  ],
  disaster:[
    {id:"DI-001",field:"evacuation_window_closed",val:false,weight:"critical",plain:"The evacuation window has closed"},
    {id:"DI-002",field:"shelter_assigned",val:true,weight:"critical",plain:"You have not been directed to a shelter or safe location"},
    {id:"DI-003",field:"comms_collapsed",val:false,weight:"major",plain:"You cannot communicate with emergency services"}
  ]
};

const GLOBAL_RULES = [
  {id:"GI-001",field:"human_authority_reachable",val:true,weight:"execution_gate",plain:"There is no one who can actually help right now"},
  {id:"GI-002",field:"time_remaining_seconds",min:1,weight:"execution_gate",plain:"Time has run out — the window for recovery has closed"},
  {id:"GI-004",field:"fallback_path_available",val:true,weight:"major",plain:"There is no backup option or alternative path"}
];

const RESULT_TEXT = {
  CONTINUE: {
    displayLabel:"CONTINUE",
    headline:"Recoverability presently established.",
    body:"Based on the conditions entered, the key conditions for recovery appear to be in place.",
    action:"Continue monitoring. Re-evaluate if conditions change."
  },
  DEGRADED: {
    displayLabel:"DEGRADED",
    headline:"Recoverability weakened.",
    body:"One or more important conditions are not fully in place. Act now before the safety margin reduces further.",
    action:"Immediate restoration of weakened conditions is required."
  },
  "NON-ADMISSIBLE": {
    displayLabel:"NON-ADMISSIBLE",
    headline:"Continuation under current conditions is not admissible.",
    body:"The conditions required for a recoverable outcome are not in place.",
    action:"Escalate now to a responsible authority. Do not continue without corrective action."
  },
  "NON-EXECUTABLE": {
    displayLabel:"EMERGENCY ESCALATION",
    headline:"Recoverable continuation is not executable in time.",
    body:"Time is running out or no responsible authority can act in time under present conditions.",
    action:"Immediate emergency escalation required."
  }
};

let currentSituation = null;
let currentState = {};
let lastRecordData = null;

function $(id){ return document.getElementById(id); }

function init(){
  renderSituationCards();
  bindNav();
  $("backHomeBtn").addEventListener("click", goHome);
  $("checkBtn").addEventListener("click", runCheck);
  $("generateRecordBtn").addEventListener("click", generateDirectRecord);
  $("countrySelect").addEventListener("change", updateCountryFlag);
  updateCountryFlag();
  registerSW();
}
document.addEventListener("DOMContentLoaded", init);

function bindNav(){
  document.querySelectorAll(".nav-tab").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".nav-tab").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      ["check","record","about"].forEach(id => $("tab-" + id).classList.add("hidden"));
      $("tab-" + btn.dataset.tab).classList.remove("hidden");
    });
  });
}

function updateCountryFlag(){
  const val = $("countrySelect").value;
  const map = {AR:"Argentina",AU:"Australia",BR:"Brazil",CA:"Canada",FR:"France",DE:"Germany",IE:"Ireland",IT:"Italy",MX:"Mexico",PT:"Portugal",ES:"Spain",GB:"United Kingdom",US:"United States",DEFAULT:"International"};
  $("countryFlag").textContent = map[val] || "";
}

function renderSituationCards(){
  const grid = $("sitGrid");
  grid.innerHTML = "";
  SITUATIONS.forEach(s => {
    const card = document.createElement("button");
    card.className = "sit-card";
    card.innerHTML = `<div class="sit-icon">${s.icon}</div><div class="sit-label">${s.label}</div><div class="sit-sub">${s.sub}</div>`;
    card.addEventListener("click", () => startSituation(s.id));
    grid.appendChild(card);
  });
}

function startSituation(id){
  currentSituation = SITUATIONS.find(s => s.id === id);
  currentState = {};
  $("qDomainLabel").textContent = currentSituation.label;
  $("sec-home").classList.remove("active");
  $("sec-result").classList.remove("active");
  $("sec-questions").classList.add("active");
  renderQuestions();
}

function renderQuestions(){
  const wrap = $("questionsContainer");
  wrap.innerHTML = "";
  const total = currentSituation.questions.length;
  currentSituation.questions.forEach((q, i) => {
    const block = document.createElement("div");
    block.className = "question-block";
    let inputHtml = "";
    if(q.yn){
      inputHtml = `
        <div class="yn-row">
          <button class="yn-btn" data-val="yes">Yes</button>
          <button class="yn-btn" data-val="no">No</button>
        </div>
      `;
    } else if(q.num){
      inputHtml = `
        <div class="num-row">
          <input class="num-input" type="number" min="0" step="1" placeholder="Enter value" />
          <span class="num-unit">${q.unit || ""}</span>
        </div>
      `;
    }
    block.innerHTML = `
      <div class="q-number">QUESTION ${i+1} / ${total}</div>
      <div class="q-text">${q.text}</div>
      ${q.sub ? `<div class="q-sub">${q.sub}</div>` : ""}
      ${inputHtml}
    `;
    wrap.appendChild(block);

    if(q.yn){
      block.querySelectorAll(".yn-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          block.querySelectorAll(".yn-btn").forEach(b => b.classList.remove("selected-yes","selected-no"));
          const key = btn.dataset.val;
          btn.classList.add(key === "yes" ? "selected-yes" : "selected-no");
          currentState[q.field] = q[key];
          updateProgress();
        });
      });
    }
    if(q.num){
      const input = block.querySelector(".num-input");
      input.addEventListener("input", () => {
        const n = Number(input.value);
        currentState[q.field] = Number.isFinite(n) ? n * (q.mult || 1) : "";
        updateProgress();
      });
    }
  });
  updateProgress();
}

function updateProgress(){
  const total = currentSituation.questions.length;
  const answered = currentSituation.questions.filter(q => currentState[q.field] !== undefined && currentState[q.field] !== "").length;
  const pct = Math.round((answered / total) * 100);
  $("progressFill").style.width = pct + "%";
  $("checkBtn").style.display = answered === total ? "block" : "none";
}

function evalRule(rule, state){
  const v = state[rule.field];
  if(v === undefined || v === null || v === "") return {passed:null, unknown:true, rule};
  let passed = true;
  if("val" in rule && v !== rule.val) passed = false;
  if("min" in rule && (isNaN(Number(v)) || Number(v) < rule.min)) passed = false;
  return {passed, unknown:false, rule};
}

function evaluate(domain, state){
  const results = [];
  for(const rule of GLOBAL_RULES) results.push(evalRule(rule, state));
  for(const rule of (DOMAIN_RULES[domain] || [])) results.push(evalRule(rule, state));

  const critFail = results.filter(r => !r.passed && !r.unknown && (r.rule.weight === "critical" || r.rule.weight === "execution_gate"));
  const majorFail = results.filter(r => !r.passed && !r.unknown && r.rule.weight === "major");
  const gateFail = results.filter(r => !r.passed && !r.unknown && r.rule.weight === "execution_gate");
  const timeLeft = Number(state.time_remaining_seconds) || 0;

  let stateOut;
  if(critFail.length){
    stateOut = (gateFail.length || timeLeft < 3600) ? "NON-EXECUTABLE" : "NON-ADMISSIBLE";
  } else if(majorFail.length){
    stateOut = "DEGRADED";
  } else {
    stateOut = "CONTINUE";
  }
  return { state: stateOut, failed: [...critFail, ...majorFail], results, timeLeft };
}

function runCheck(){
  const result = evaluate(currentSituation.id, currentState);
  renderResult(currentSituation, currentState, result);
  $("sec-questions").classList.remove("active");
  $("sec-result").classList.add("active");
}

function renderResult(sit, state, result){
  const txt = RESULT_TEXT[result.state];
  const hours = result.timeLeft ? Math.round(result.timeLeft / 3600) : 0;
  const failLines = result.failed.map(f => `${f.rule.id} — ${f.rule.plain}`);
  const recordData = buildFormalRecordData(sit, state, result);
  lastRecordData = recordData;

  $("resultContent").innerHTML = `
    <div class="result-state ${result.state}">
      <div class="result-label">${txt.displayLabel}</div>
      <div class="result-headline">${txt.headline}</div>
      <div class="result-body">${txt.body}</div>
    </div>

    <div class="result-action">
      <div class="result-action-label">Required action</div>
      <div class="result-action-text">${txt.action}</div>
    </div>

    ${failLines.length ? `
      <div class="result-fails">
        <div class="result-fails-label">Conditions that failed</div>
        ${failLines.map(f => `<div class="fail-item">${f}</div>`).join("")}
      </div>
    ` : ""}

    <div class="record-preview-card">
      <div class="fr-label">Formal record preview</div>
      <div class="fr-section-title" style="margin-top:8px;">Who must act now</div>
      <p>${recordData.authority}</p>
      <div class="fr-section-title" style="margin-top:14px;">Maximum response window</div>
      <p>${recordData.responseWindow}</p>
      <div class="fr-section-title" style="margin-top:14px;">If no action occurs in time</div>
      <p>${recordData.nextEscalation}</p>
      <button class="pdf-btn" id="downloadRecordBtn" style="margin-top:16px;">↓ Download formal record</button>
    </div>

    <button class="again-btn" id="againBtn">Start again</button>

    <div class="result-timestamp">
      Evaluated: ${recordData.date} at ${recordData.time}<br>
      Domain: ${sit.label}<br>
      Framework DOI: 10.5281/zenodo.19583410
    </div>
  `;

  $("downloadRecordBtn").addEventListener("click", () => downloadFormalRecord(recordData));
  $("againBtn").addEventListener("click", goHome);
}

function buildFormalRecordData(sit, state, result){
  const dt = new Date();
  const date = dt.toLocaleDateString("en-GB",{day:"2-digit",month:"long",year:"numeric"});
  const time = dt.toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit"});
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "Local";
  const country = $("countrySelect").options[$("countrySelect").selectedIndex]?.text || "Not stated";
  const statusMap = result.timeLeft <= 0 ? "EXPIRED" : result.timeLeft < 3600 ? "CRITICAL" : result.timeLeft < 14400 ? "REDUCED" : "ADEQUATE";
  const authority = sit.authority;
  const responseWindow = result.timeLeft ? `${Math.max(1, Math.round(result.timeLeft/3600))} hour(s)` : "Immediate";
  const stateText = RESULT_TEXT[result.state];
  const summary = `A ${sit.label.toLowerCase()} was evaluated under present conditions. At the time of evaluation, ${stateText.body.toLowerCase()}`;
  const verification = (crypto.randomUUID ? crypto.randomUUID().slice(0,8) : Math.random().toString(36).slice(2,10)).toUpperCase();
  const recordId = `REC-${dt.getFullYear()}${String(dt.getMonth()+1).padStart(2,"0")}${String(dt.getDate()).padStart(2,"0")}-${verification}`;
  const nextEscalation = result.state === "NON-EXECUTABLE"
    ? "Escalate immediately to emergency services or highest available responsible authority."
    : "Escalate to the next responsible authority if no corrective action occurs within the response window.";

  return {
    recordId,
    evalId: verification,
    date,
    time,
    timezone: tz,
    country,
    domain: sit.label,
    state: result.state,
    stateLabel: stateText.displayLabel,
    headline: stateText.headline,
    body: stateText.body,
    requiredAction: stateText.action,
    timeStatus: statusMap,
    timeRemaining: result.timeLeft ? `${Math.round(result.timeLeft/3600)} hour(s)` : "Expired / not stated",
    summary,
    authority,
    formAction: result.state === "CONTINUE" ? "Monitor and re-evaluate" :
      result.state === "DEGRADED" ? "Restore weakened conditions" :
      result.state === "NON-ADMISSIBLE" ? "Escalate and restore recoverable conditions" :
      "Immediate emergency escalation",
    responseWindow,
    nextEscalation,
    failedConditions: result.failed.map(f => ({
      code: f.rule.id,
      plain: f.rule.plain,
      observed: String(state[f.rule.field]),
      weight: f.rule.weight
    })),
    escalationChain: [
      authority,
      "Secondary responsible authority / service lead",
      "Independent authority / emergency channel",
      "External regulatory or public escalation if unresolved"
    ],
    subject: "Self-reported evaluation",
    role: "User",
    institution: "Not stated",
    notice: result.state === "NON-EXECUTABLE"
      ? "Recoverable continuation is not executable in time under present conditions. Immediate escalation is required now."
      : result.state === "NON-ADMISSIBLE"
      ? "Continuation under present conditions is not admissible. A responsible authority must act without delay."
      : result.state === "DEGRADED"
      ? "Recoverability is weakened. Immediate restoration is required."
      : "Recoverability presently appears established under the entered conditions.",
    verification
  };
}

function downloadFormalRecord(data){
  const failedHtml = data.failedConditions.map(item => `
    <div class="fr-fail"><strong>${item.code} — ${item.plain}</strong><br>
    Observed state: ${item.observed}<br>
    Effect on admissibility: ${item.weight}</div>
  `).join("");

  const chainHtml = data.escalationChain.map(x => `<li>${x}</li>`).join("");

  const stateClass = data.state === "CONTINUE" ? "continue" :
    data.state === "DEGRADED" ? "degraded" :
    data.state === "NON-ADMISSIBLE" ? "non-admissible" : "non-executable";

  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"/>
  <title>${data.recordId}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@300;600;700&family=DM+Mono:wght@400;500&display=swap');
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Fraunces',Georgia,serif;color:#0f0f0f;background:#fff;padding:42px;max-width:760px;margin:0 auto;line-height:1.55}
    .fr-header{border-bottom:2px solid #0f0f0f;padding-bottom:16px;margin-bottom:18px}
    .fr-kicker,.fr-section-title{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#6b6560}
    .fr-title{font-size:28px;font-weight:700;line-height:1.15;margin-top:8px}
    .fr-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;margin:16px 0 18px}
    .fr-state-box{border:3px solid #0f0f0f;border-radius:8px;padding:18px;margin-bottom:18px}
    .fr-state-box.non-admissible{border-color:#c0392b}
    .fr-state-box.non-executable{border-color:#6d28d9}
    .fr-state-box.degraded{border-color:#d97706}
    .fr-state-box.continue{border-color:#1a6b3c}
    .fr-state-value{font-size:32px;font-weight:700;margin-bottom:8px}
    .fr-action-value{font-size:18px;font-weight:700;margin:8px 0 12px}
    .fr-time-row{display:flex;gap:20px;flex-wrap:wrap;font-family:'DM Mono',monospace;font-size:12px;color:#6b6560}
    .fr-section{margin-bottom:18px}
    .fr-fail{border-left:4px solid #c0392b;background:#f8f8f8;padding:10px 12px;margin-top:10px}
    .fr-footer{border-top:1px solid #d4cdc4;padding-top:14px;margin-top:18px;font-family:'DM Mono',monospace;font-size:12px;color:#6b6560;line-height:1.7}
    ol{padding-left:20px}
    li{margin-bottom:6px}
    @media print{body{padding:20px}}
  </style></head><body>
    <div class="fr-header">
      <div class="fr-kicker">RECOVS FORMAL RECORD</div>
      <div class="fr-title">Recoverability Evaluation and Admissibility Determination</div>
    </div>

    <div class="fr-grid">
      <div><strong>Record ID:</strong> ${data.recordId}</div>
      <div><strong>Evaluation ID:</strong> ${data.evalId}</div>
      <div><strong>Date:</strong> ${data.date}</div>
      <div><strong>Time:</strong> ${data.time}</div>
      <div><strong>Timezone:</strong> ${data.timezone}</div>
      <div><strong>Country / Jurisdiction:</strong> ${data.country}</div>
      <div><strong>Domain:</strong> ${data.domain}</div>
      <div><strong>Verification:</strong> ${data.verification}</div>
    </div>

    <div class="fr-state-box ${stateClass}">
      <div class="fr-kicker">State</div>
      <div class="fr-state-value">${data.stateLabel}</div>
      <div>${data.headline} ${data.body}</div>
      <div class="fr-kicker" style="margin-top:14px;">Required action</div>
      <div class="fr-action-value">${data.requiredAction}</div>
      <div class="fr-time-row">
        <div><strong>Time status:</strong> ${data.timeStatus}</div>
        <div><strong>Time remaining:</strong> ${data.timeRemaining}</div>
      </div>
    </div>

    <div class="fr-section">
      <div class="fr-section-title">Admissibility Condition</div>
      <p>A situation may continue only while recoverability can be established in time under real conditions.
      Where recoverability cannot be established, verified, interpreted, enforced, or executed within the available
      time before irreversible transition, continuation is non-admissible and execution does not occur.</p>
    </div>

    <div class="fr-section">
      <div class="fr-section-title">Situation Summary</div>
      <p>${data.summary}</p>
    </div>

    <div class="fr-section">
      <div class="fr-section-title">Failed Conditions Identified</div>
      ${failedHtml || "<p>No failed conditions recorded.</p>"}
    </div>

    <div class="fr-section">
      <div class="fr-section-title">Who Must Act Now</div>
      <p><strong>Primary responsible authority:</strong> ${data.authority}</p>
      <p><strong>Required form of action:</strong> ${data.formAction}</p>
      <p><strong>Maximum response window:</strong> ${data.responseWindow}</p>
      <p><strong>If no action occurs in time:</strong> ${data.nextEscalation}</p>
    </div>

    <div class="fr-section">
      <div class="fr-section-title">Escalation Chain</div>
      <ol>${chainHtml}</ol>
    </div>

    <div class="fr-section">
      <div class="fr-section-title">Immediate Notice</div>
      <p>${data.notice}</p>
    </div>

    <div class="fr-footer">
      Framework DOI: doi.org/10.5281/zenodo.19583410<br>
      Generated by: RECOVS<br>
      This record evaluates recoverability only. It does not make or enforce clinical, legal, financial, or operational decisions.
      All outputs require action by a responsible human authority.
    </div>
  </body></html>`;

  const win = window.open("", "_blank");
  if(win){
    win.document.write(html);
    win.document.close();
    setTimeout(() => win.print(), 500);
  } else {
    const a = document.createElement("a");
    a.href = "data:text/html;charset=utf-8," + encodeURIComponent(html);
    a.download = `${data.recordId}.html`;
    a.click();
  }
}

function generateDirectRecord(){
  const reporter = $("fr-reporter").value.trim();
  const role = $("fr-role").value.trim();
  const institution = $("fr-institution").value.trim();
  const what = $("fr-what").value.trim();
  const subject = $("fr-subject").value.trim();

  const dt = new Date();
  const code = (crypto.randomUUID ? crypto.randomUUID().slice(0,8) : Math.random().toString(36).slice(2,10)).toUpperCase();
  const record = {
    recordId: `REC-DIRECT-${code}`,
    evalId: code,
    date: dt.toLocaleDateString("en-GB",{day:"2-digit",month:"long",year:"numeric"}),
    time: dt.toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit"}),
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "Local",
    country: $("countrySelect").options[$("countrySelect").selectedIndex]?.text || "Not stated",
    domain: "Direct formal record",
    state: "NON-ADMISSIBLE",
    stateLabel: "NON-ADMISSIBLE",
    headline: "Continuation under current conditions is not admissible.",
    body: "A contemporaneous formal record has been created for responsible review and escalation.",
    requiredAction: "Escalate now to a responsible authority and preserve this record.",
    timeStatus: "NOT STATED",
    timeRemaining: "Not stated",
    summary: what || "Formal record generated without structured evaluation answers.",
    authority: institution || "Responsible authority / institution",
    formAction: "Review, acknowledge, and act",
    responseWindow: "As soon as possible",
    nextEscalation: "Escalate to the next available authority if no acknowledgment or action occurs.",
    failedConditions: what ? [{code:"DR-001",plain:"Reported interruption or denial condition recorded",observed:"Reported by user",weight:"critical"}] : [],
    escalationChain: [
      institution || "Primary institution or service",
      "Service lead / supervisor",
      "Independent authority / external reviewer",
      "Emergency or legal escalation if delay creates irrecoverable loss"
    ],
    subject: subject || "Not stated",
    role: role || "Not stated",
    institution: institution || "Not stated",
    notice: "This record preserves a contemporaneous statement for responsible review. If conditions are time-critical, escalation should not be delayed.",
    verification: code
  };
  lastRecordData = record;
  $("recordPreview").classList.remove("hidden");
  $("recordPreview").innerHTML = `
    <div class="formal-record">
      <div class="fr-header">
        <div class="fr-kicker">RECOVS FORMAL RECORD</div>
        <div class="fr-title">Direct formal record preview</div>
      </div>
      <div class="fr-grid fr-meta">
        <div><strong>Record ID:</strong> ${record.recordId}</div>
        <div><strong>Date:</strong> ${record.date}</div>
        <div><strong>Reporter:</strong> ${reporter || "Not stated"}</div>
        <div><strong>Role:</strong> ${role || "Not stated"}</div>
      </div>
      <div class="fr-section">
        <div class="fr-section-title">What happened</div>
        <p>${what || "Not stated"}</p>
      </div>
      <div class="fr-section">
        <div class="fr-section-title">Institution / service involved</div>
        <p>${institution || "Not stated"}</p>
      </div>
      <button class="pdf-btn" id="downloadDirectRecordBtn">↓ Download formal record</button>
    </div>
  `;
  $("downloadDirectRecordBtn").addEventListener("click", () => downloadFormalRecord(record));
}

function goHome(){
  $("sec-questions").classList.remove("active");
  $("sec-result").classList.remove("active");
  $("sec-home").classList.add("active");
  window.scrollTo({top:0,behavior:"smooth"});
}

async function registerSW(){
  if(!("serviceWorker" in navigator)) return;
  try { await navigator.serviceWorker.register("sw.js"); } catch(e) { console.log("SW unavailable", e); }
}