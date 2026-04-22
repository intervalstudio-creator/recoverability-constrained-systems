const STORAGE_KEYS = {
  country: "recovs-country",
  activeTab: "recovs-active-tab",
  draftRecord: "recovs-direct-record-draft",
  lastSituation: "recovs-last-situation",
  profile: "recovs-profile",
  history: "recovs-history",
  trusted: "recovs-trusted",
  checkin: "recovs-checkin"
};

const SITUATIONS = [
  {
    id: "pharmacological",
    icon: "💊",
    label: "Medication problem",
    sub: "Prescription / supply",
    authority: "Prescriber, pharmacist, urgent care, emergency service",
    questions: [
      { id: "q1", text: "Do you have enough medication to last the next few days?", sub: "Include pills, patches, injections, or other forms.", yn: true, field: "supply_days_remaining", yes: 7, no: 0 },
      { id: "q2", text: "Can you reach your doctor or prescriber right now?", sub: "By phone, online, or in person.", yn: true, field: "prescriber_reachable", yes: true, no: false },
      { id: "q3", text: "Would stopping this medication suddenly be dangerous?", sub: "Examples: benzodiazepines, insulin, epilepsy, or heart medication.", yn: true, field: "abrupt_stop_risk", yes: true, no: false },
      { id: "q4", text: "Can you get to a pharmacy or have medication delivered?", yn: true, field: "dispensing_accessible", yes: true, no: false },
      { id: "q5", text: "Is there any backup option: urgent clinic, emergency prescription, or out-of-hours doctor?", yn: true, field: "fallback_path_available", yes: true, no: false },
      { id: "q6", text: "Is there someone who can actually help right now?", yn: true, field: "human_authority_reachable", yes: true, no: false },
      { id: "q7", text: "How many hours before this becomes a serious emergency if nothing changes?", num: true, field: "time_remaining_seconds", unit: "hours", mult: 3600 }
    ]
  },
  {
    id: "healthcare",
    icon: "🏥",
    label: "Healthcare problem",
    sub: "Appointment / care / hospital",
    authority: "Hospital, responsible clinician, emergency service",
    questions: [
      { id: "q1", text: "Have you missed or are you about to miss a critical medical appointment?", yn: true, field: "critical_appointment_missed", yes: true, no: false },
      { id: "q2", text: "Do you have a way to get to the hospital or clinic if needed?", yn: true, field: "transport_available", yes: true, no: false },
      { id: "q3", text: "Is your carer or support person available right now?", yn: true, field: "caregiver_available", yes: true, no: false },
      { id: "q4", text: "Can you reach a doctor, nurse, or emergency service right now?", yn: true, field: "human_authority_reachable", yes: true, no: false },
      { id: "q5", text: "Is there an alternative such as a different hospital, home visit, or urgent helpline?", yn: true, field: "fallback_path_available", yes: true, no: false },
      { id: "q6", text: "How many hours before this becomes a serious emergency?", num: true, field: "time_remaining_seconds", unit: "hours", mult: 3600 }
    ]
  },
  {
    id: "finance",
    icon: "💳",
    label: "Money / bank problem",
    sub: "Account / payment / benefits",
    authority: "Bank, welfare service, housing authority, emergency support service",
    questions: [
      { id: "q1", text: "Is your bank account locked or frozen?", yn: true, field: "bank_locked", yes: true, no: false },
      { id: "q2", text: "Are you unable to pay for something essential: rent, food, medication, or utilities?", yn: true, field: "essential_payment_blocked", yes: true, no: false },
      { id: "q3", text: "Has your income, wages, or benefits stopped or been delayed?", yn: true, field: "income_interrupted", yes: true, no: false },
      { id: "q4", text: "Can you reach your bank, welfare service, or someone who can help right now?", yn: true, field: "human_authority_reachable", yes: true, no: false },
      { id: "q5", text: "Is there any alternative such as a different account, family help, or crisis fund?", yn: true, field: "fallback_path_available", yes: true, no: false },
      { id: "q6", text: "How many hours before you face a serious consequence?", num: true, field: "time_remaining_seconds", unit: "hours", mult: 3600 }
    ]
  },
  {
    id: "housing",
    icon: "🏠",
    label: "Housing problem",
    sub: "Eviction / shelter / utilities",
    authority: "Housing office, council, emergency accommodation service",
    questions: [
      { id: "q1", text: "Are you facing eviction or being forced to leave your home?", yn: true, field: "eviction_imminent", yes: true, no: false },
      { id: "q2", text: "Have your gas, electricity, or water been cut off?", yn: true, field: "utilities_disconnected", yes: true, no: false },
      { id: "q3", text: "Is your home currently unsafe or uninhabitable?", yn: true, field: "habitability_failure", yes: true, no: false },
      { id: "q4", text: "Can you reach a housing officer or emergency housing service right now?", yn: true, field: "human_authority_reachable", yes: true, no: false },
      { id: "q5", text: "Is there anywhere else you could go: family, shelter, or emergency accommodation?", yn: true, field: "fallback_path_available", yes: true, no: false },
      { id: "q6", text: "How many hours before this becomes a crisis?", num: true, field: "time_remaining_seconds", unit: "hours", mult: 3600 }
    ]
  },
  {
    id: "identity",
    icon: "🪪",
    label: "Identity / documents",
    sub: "Lost ID / locked out of services",
    authority: "Identity office, employer, bank, service provider",
    questions: [
      { id: "q1", text: "Have you lost your identity documents: passport, licence, or ID card?", yn: true, field: "id_document_available", yes: false, no: true },
      { id: "q2", text: "Are you locked out of essential accounts or services because of missing ID?", yn: true, field: "access_recovery_available", yes: false, no: true },
      { id: "q3", text: "Is your ability to receive wages or benefits affected?", yn: true, field: "payroll_identity_intact", yes: false, no: true },
      { id: "q4", text: "Can you reach a government office, employer, or recovery service right now?", yn: true, field: "human_authority_reachable", yes: true, no: false },
      { id: "q5", text: "Is there any alternative way to prove identity for now?", yn: true, field: "fallback_path_available", yes: true, no: false },
      { id: "q6", text: "How many hours before this causes a serious problem?", num: true, field: "time_remaining_seconds", unit: "hours", mult: 3600 }
    ]
  },
  {
    id: "disaster",
    icon: "⚠️",
    label: "Emergency / disaster",
    sub: "Evacuation / safety / crisis",
    authority: "Emergency service, shelter authority, crisis support",
    questions: [
      { id: "q1", text: "Is there still time to reach safety or evacuate?", yn: true, field: "evacuation_window_closed", yes: false, no: true },
      { id: "q2", text: "Have you been directed to a shelter or safe location?", yn: true, field: "shelter_assigned", yes: true, no: false },
      { id: "q3", text: "Have you lost the ability to communicate with emergency services or family?", yn: true, field: "comms_collapsed", yes: true, no: false },
      { id: "q4", text: "Can you reach emergency services or someone who can help right now?", yn: true, field: "human_authority_reachable", yes: true, no: false },
      { id: "q5", text: "Is there a route or plan that still leads to safety?", yn: true, field: "fallback_path_available", yes: true, no: false },
      { id: "q6", text: "How many hours before the situation becomes irreversible?", num: true, field: "time_remaining_seconds", unit: "hours", mult: 3600 }
    ]
  }
];

const DOMAIN_RULES = {
  pharmacological: [
    { id: "PH-001", field: "supply_days_remaining", min: 1, weight: "critical", plain: "Medication supply has run out or will run out imminently" },
    { id: "PH-002", field: "prescriber_reachable", val: true, weight: "critical", plain: "You cannot reach your prescriber" },
    { id: "PH-003", field: "abrupt_stop_risk", val: false, weight: "critical", plain: "Stopping this medication suddenly is dangerous" },
    { id: "PH-004", field: "dispensing_accessible", val: true, weight: "major", plain: "You cannot access a pharmacy or delivery" }
  ],
  healthcare: [
    { id: "HC-001", field: "critical_appointment_missed", val: false, weight: "critical", plain: "A critical appointment has been or will be missed" },
    { id: "HC-002", field: "transport_available", val: true, weight: "major", plain: "You have no way to get to hospital or clinic" },
    { id: "HC-003", field: "caregiver_available", val: true, weight: "critical", plain: "Your carer or support person is not available" }
  ],
  finance: [
    { id: "FI-001", field: "bank_locked", val: false, weight: "critical", plain: "Your bank account is locked or frozen" },
    { id: "FI-002", field: "essential_payment_blocked", val: false, weight: "critical", plain: "You cannot pay for essential needs" },
    { id: "FI-003", field: "income_interrupted", val: false, weight: "major", plain: "Income or benefits have stopped or been delayed" }
  ],
  housing: [
    { id: "HO-001", field: "eviction_imminent", val: false, weight: "critical", plain: "You are facing imminent eviction" },
    { id: "HO-002", field: "utilities_disconnected", val: false, weight: "major", plain: "Utilities have been cut off" },
    { id: "HO-003", field: "habitability_failure", val: false, weight: "critical", plain: "Your home is unsafe or uninhabitable" }
  ],
  identity: [
    { id: "ID-001", field: "id_document_available", val: true, weight: "major", plain: "Identity documents are not available" },
    { id: "ID-002", field: "access_recovery_available", val: true, weight: "major", plain: "You are locked out of essential services due to missing ID" },
    { id: "ID-003", field: "payroll_identity_intact", val: true, weight: "major", plain: "Ability to receive wages or benefits is affected" }
  ],
  disaster: [
    { id: "DI-001", field: "evacuation_window_closed", val: false, weight: "critical", plain: "The evacuation window has closed" },
    { id: "DI-002", field: "shelter_assigned", val: true, weight: "critical", plain: "You have not been directed to a shelter or safe location" },
    { id: "DI-003", field: "comms_collapsed", val: false, weight: "major", plain: "You cannot communicate with emergency services" }
  ]
};

const GLOBAL_RULES = [
  { id: "GI-001", field: "human_authority_reachable", val: true, weight: "execution_gate", plain: "There is no one who can actually help right now" },
  { id: "GI-002", field: "time_remaining_seconds", min: 1, weight: "execution_gate", plain: "Time has run out: the window for recovery has closed" },
  { id: "GI-004", field: "fallback_path_available", val: true, weight: "major", plain: "There is no backup option or alternative path" }
];

const RESULT_TEXT = {
  CONTINUE: {
    displayLabel: "ADMISSIBLE",
    headline: "Recoverability presently established.",
    body: "Based on the conditions entered, the key conditions for recovery appear to be in place.",
    action: "Continue monitoring and re-evaluate if conditions change."
  },
  DEGRADED: {
    displayLabel: "DEGRADED",
    headline: "Recoverability is weakened.",
    body: "One or more important conditions are not fully in place. Act now before the safety margin reduces further.",
    action: "Immediate restoration of weakened conditions is required."
  },
  "NON-ADMISSIBLE": {
    displayLabel: "NON-ADMISSIBLE",
    headline: "Continuation under current conditions is not admissible.",
    body: "The conditions required for a recoverable outcome are not in place.",
    action: "Escalate now to a responsible authority. Do not continue without corrective action."
  },
  "NON-EXECUTABLE": {
    displayLabel: "NON-EXECUTABLE",
    headline: "Recoverable continuation is not executable in time.",
    body: "Time is running out or no responsible authority can act in time under present conditions.",
    action: "Immediate emergency escalation is required."
  }
};

const CRISIS_ORGS = {
  GB: {
    pharmacological: [
      { name: "NHS 111", contact: "111", type: "phone", note: "Urgent medical advice including medication." },
      { name: "CALM", contact: "0800 58 58 58", type: "phone", note: "Crisis support, evenings." }
    ],
    healthcare: [
      { name: "NHS 111", contact: "111", type: "phone", note: "Urgent medical advice." },
      { name: "Samaritans", contact: "116 123", type: "phone", note: "24/7 emotional support." }
    ],
    finance: [
      { name: "Citizens Advice", contact: "0800 144 8848", type: "phone", note: "Benefits, debt, and money support." },
      { name: "Turn2us", contact: "0808 802 2000", type: "phone", note: "Emergency grants and benefits." }
    ],
    housing: [
      { name: "Shelter", contact: "0808 800 4444", type: "phone", note: "Emergency housing support." },
      { name: "St Mungo's", contact: "020 3856 6000", type: "phone", note: "Homelessness support." }
    ],
    identity: [
      { name: "Victim Support", contact: "08 08 16 89 111", type: "phone", note: "Support if ID was lost due to crime." }
    ],
    disaster: [
      { name: "999", contact: "999", type: "phone", note: "Police, ambulance, or fire." },
      { name: "Red Cross UK", contact: "0344 871 11 11", type: "phone", note: "Disaster relief support." }
    ],
    default: [
      { name: "Samaritans", contact: "116 123", type: "phone", note: "Any crisis, 24/7, free." }
    ]
  },
  AR: {
    pharmacological: [
      { name: "SAME", contact: "107", type: "phone", note: "Emergencia medica." }
    ],
    healthcare: [
      { name: "SIES", contact: "107", type: "phone", note: "Sistema de emergencias." },
      { name: "Centro de Asistencia al Suicida", contact: "135", type: "phone", note: "Crisis emocional 24 horas." }
    ],
    finance: [
      { name: "ANSES", contact: "130", type: "phone", note: "Beneficios sociales." },
      { name: "Defensoria del Pueblo", contact: "0800 444 3362", type: "phone", note: "Defensa de derechos y reclamos." }
    ],
    housing: [
      { name: "Ministerio de Desarrollo Social", contact: "0800 222 3294", type: "phone", note: "Emergencia habitacional." }
    ],
    default: [
      { name: "Centro de Asistencia al Suicida", contact: "135", type: "phone", note: "Crisis emocional, gratuito." }
    ]
  },
  US: {
    pharmacological: [
      { name: "Poison Control", contact: "1-800-222-1222", type: "phone", note: "Medication emergencies." },
      { name: "Crisis Text Line", contact: "Text HOME to 741741", type: "text", note: "Text support for crisis." }
    ],
    healthcare: [
      { name: "911", contact: "911", type: "phone", note: "Medical emergency." },
      { name: "SAMHSA", contact: "1-800-662-4357", type: "phone", note: "Mental health and substance use support." }
    ],
    finance: [
      { name: "211", contact: "211", type: "phone", note: "Local welfare and housing resources." },
      { name: "CFPB", contact: "1-855-411-2372", type: "phone", note: "Banking complaints and assistance." }
    ],
    housing: [
      { name: "211", contact: "211", type: "phone", note: "Shelter and housing referrals." },
      { name: "HUD", contact: "1-800-569-4287", type: "phone", note: "Housing counseling." }
    ],
    default: [
      { name: "988 Lifeline", contact: "988", type: "phone", note: "Suicide and crisis, 24/7." }
    ]
  },
  DEFAULT: {
    default: [
      { name: "International emergency", contact: "112", type: "phone", note: "Works in many countries." },
      { name: "WHO mental health", contact: "https://www.who.int/health-topics/mental-health", type: "link", note: "Find local crisis support." }
    ]
  }
};

let currentSituation = null;
let currentState = {};
let lastRecordData = null;
let groupMembers = [];
let checkinTimer = null;
let checkinData = null;
let nextCheckin = null;
let childAnswers = {};
let currentRecordMode = "self";

function $(id){
  return document.getElementById(id);
}

function init(){
  renderSituationCards();
  bindNav();
  initRecordModes();
  bindRecordDraftPersistence();
  bindOutreachTools();
  bindExtendedTools();
  $("backHomeBtn").addEventListener("click", goHome);
  $("checkBtn").addEventListener("click", runCheck);
  $("generateRecordBtn").addEventListener("click", generateDirectRecord);
  $("countrySelect").addEventListener("change", onCountryChange);

  restoreCountry();
  restoreActiveTab();
  restoreDraftRecord();
  loadProfile();
  prefillFromProfile(loadProfile());
  loadTrustedContact();
  renderHistory();
  renderGroupSummary();
  updateLockCardPreview();
  restoreCheckin();
  updateCountryFlag();
  registerSW();
}

document.addEventListener("DOMContentLoaded", init);

function bindNav(){
  document.querySelectorAll(".nav-tab").forEach((btn) => {
    if(btn.dataset.tab){
      btn.addEventListener("click", () => setActiveTab(btn.dataset.tab));
    }
  });
}

function bindOutreachTools(){
  const copyLineBtn = $("copyInstitutionLineBtn");
  const examplePdfBtn = $("downloadExamplePdfBtn");

  if(copyLineBtn){
    copyLineBtn.addEventListener("click", copyInstitutionLine);
  }
  if(examplePdfBtn){
    examplePdfBtn.addEventListener("click", async () => {
      await downloadExamplePdf();
    });
  }
}

function setActiveTab(tabId){
  if(tabId === "behalf" || tabId === "witness"){
    setRecordMode(tabId);
    tabId = "record";
  }
  if(tabId === "lock"){
    tabId = "profile";
  }

  document.querySelectorAll(".nav-tab").forEach((btn) => {
    if(!btn.dataset.tab) return;
    const isActive = btn.dataset.tab === tabId;
    btn.classList.toggle("active", isActive);
    btn.setAttribute("aria-selected", String(isActive));
  });

  ["check", "record", "lock", "behalf", "witness", "child", "checkin", "profile", "trusted", "group", "about"].forEach((id) => {
    const el = $("tab-" + id);
    if(el){
      el.classList.toggle("hidden", id !== tabId);
    }
  });

  if(tabId === "profile") renderHistory();
  if(tabId === "group") renderGroupSummary();
  if(tabId === "child") resetChildFlow();
  if(tabId === "record") setRecordMode(currentRecordMode);
  safeSetStorage(STORAGE_KEYS.activeTab, tabId);
}

function initRecordModes(){
  document.querySelectorAll(".record-mode-tab").forEach((btn) => {
    btn.addEventListener("click", () => setRecordMode(btn.dataset.recordMode));
  });

  const behalfTab = $("tab-behalf");
  const behalfTarget = $("recordMode-behalf");
  if(behalfTab && behalfTarget){
    behalfTarget.innerHTML = behalfTab.innerHTML;
  }

  const witnessTab = $("tab-witness");
  const witnessTarget = $("recordMode-witness");
  if(witnessTab && witnessTarget){
    witnessTarget.innerHTML = witnessTab.innerHTML;
  }

  setRecordMode("self");
}

function setRecordMode(mode){
  currentRecordMode = mode;

  document.querySelectorAll(".record-mode-tab").forEach((btn) => {
    const isActive = btn.dataset.recordMode === mode;
    btn.classList.toggle("active", isActive);
    btn.setAttribute("aria-pressed", String(isActive));
  });

  ["self", "behalf", "witness"].forEach((key) => {
    const panel = $("recordMode-" + key);
    if(panel){
      panel.classList.toggle("hidden", key !== mode);
    }
  });
}

function bindExtendedTools(){
  $("saveProfileBtn").addEventListener("click", saveProfile);
  $("clearProfileBtn").addEventListener("click", clearProfile);
  $("saveTrustedBtn").addEventListener("click", saveTrustedContact);
  $("sendEmailAlertBtn").addEventListener("click", sendEmailAlert);
  $("sendSmsAlertBtn").addEventListener("click", sendSmsAlert);
  $("addGroupMemberBtn").addEventListener("click", addGroupMember);
  $("downloadGroupReportBtn").addEventListener("click", downloadGroupReport);
  $("downloadLockCardBtn").addEventListener("click", downloadLockCard);
  $("generateBehalfBtn").addEventListener("click", generateBehalfRecord);
  $("generateWitnessBtn").addEventListener("click", generateWitnessRecord);
  $("startCheckinBtn").addEventListener("click", startCheckin);
  $("generateChildReportBtn").addEventListener("click", generateChildReport);
  $("childQ1Yes").addEventListener("click", () => childAnswer(1, "yes"));
  $("childQ1No").addEventListener("click", () => childAnswer(1, "no"));
  $("childQ2Yes").addEventListener("click", () => childAnswer(2, "yes"));
  $("childQ2No").addEventListener("click", () => childAnswer(2, "no"));
  $("childQ3Yes").addEventListener("click", () => childAnswer(3, "yes"));
  $("childQ3No").addEventListener("click", () => childAnswer(3, "no"));

  ["ls-name", "ls-dob", "ls-blood", "ls-meds", "ls-allergies", "ls-ec1", "ls-ec2", "ls-note"].forEach((id) => {
    $(id).addEventListener("input", updateLockCardPreview);
    $(id).addEventListener("change", updateLockCardPreview);
  });
}

function childAnswer(step, answer){
  childAnswers[step] = answer;

  if(step === 1){
    $("childStep1").classList.add("hidden");
    if(answer === "no"){
      showChildResult("safe");
      return;
    }
    $("childStep2").classList.remove("hidden");
    return;
  }

  if(step === 2){
    $("childStep2").classList.add("hidden");
    if(answer === "no"){
      showChildResult("unsafe");
      return;
    }
    $("childStep3").classList.remove("hidden");
    return;
  }

  $("childStep3").classList.add("hidden");
  showChildResult(answer === "yes" ? "adult-present" : "alone");
}

function showChildResult(type){
  const country = $("countrySelect").value || "DEFAULT";
  const emergencyNumber = country === "GB" ? "999" : country === "US" || country === "AR" ? "911" : "112";
  const result = $("childResult");
  const variants = {
    safe: {
      cls: "safe",
      icon: "🌟",
      title: "You are okay.",
      body: "You are safe right now. If something changes, tell a grown-up.",
      action: ""
    },
    unsafe: {
      cls: "help",
      icon: "🆘",
      title: "You need help now.",
      body: "You are not in a safe place. Get help from a grown-up or emergency service now.",
      action: `Call ${emergencyNumber} now.`
    },
    "adult-present": {
      cls: "safe",
      icon: "🧑‍🤝‍🧑",
      title: "Ask the grown-up for help.",
      body: "Show this screen to the grown-up near you and tell them you need help.",
      action: ""
    },
    alone: {
      cls: "help",
      icon: "📞",
      title: "Call for help now.",
      body: "There is no grown-up nearby. Call the emergency number and say where you are.",
      action: `Call ${emergencyNumber} now.`
    }
  };

  const selected = variants[type];
  result.className = "child-result " + selected.cls;
  result.innerHTML = `
    <div class="child-emoji" aria-hidden="true">${selected.icon}</div>
    <div class="child-result-title">${escapeHtml(selected.title)}</div>
    <div class="child-result-body">${escapeHtml(selected.body)}</div>
    ${selected.action ? `<div class="child-result-title child-reset">${escapeHtml(selected.action)}</div>` : ""}
    <button class="again-btn child-reset" type="button" id="childResetBtn">Start again</button>
  `;
  result.classList.remove("hidden");
  $("childResetBtn").addEventListener("click", resetChildFlow);
}

function resetChildFlow(){
  childAnswers = {};
  $("childStep1").classList.remove("hidden");
  $("childStep2").classList.add("hidden");
  $("childStep3").classList.add("hidden");
  $("childResult").className = "child-result hidden";
  $("childResult").innerHTML = "";
}

function generateChildReport(){
  const name = $("child-name").value.trim();
  const age = $("child-age").value.trim();
  const where = $("child-where").value.trim();
  const withWho = $("child-with").value.trim();
  const what = $("child-what").value.trim();
  const helpNow = $("child-help-now").value;

  if(!what && !where){
    announce("Add what happened or where you are to make the child report.");
    return;
  }

  const now = new Date();
  const country = $("countrySelect").value || "DEFAULT";
  const emergencyNumber = country === "GB" ? "999" : country === "US" || country === "AR" ? "911" : "112";
  const evalId = `RECOVS-CHILD-${now.getTime().toString(36).toUpperCase()}`;
  const helpLabel = helpNow === "yes" ? "Yes" : helpNow === "not_sure" ? "Not sure" : helpNow === "no" ? "No" : "Not stated";

  const preview = $("childReportPreview");
  preview.classList.remove("hidden");
  preview.innerHTML = `
    <div class="record-preview-card">
      <div class="hero-panel-label">Child report</div>
      <div class="formal-record">
        <div class="fr-section-title">Reference</div>
        <div class="fr-grid">
          <div><strong>Evaluation ID:</strong> ${escapeHtml(evalId)}</div>
          <div><strong>Timestamp:</strong> ${escapeHtml(now.toISOString())}</div>
          <div><strong>Name:</strong> ${escapeHtml(name || "Not given")}</div>
          <div><strong>Age:</strong> ${escapeHtml(age || "Not given")}</div>
          <div><strong>Where:</strong> ${escapeHtml(where || "Not given")}</div>
          <div><strong>Who is with you:</strong> ${escapeHtml(withWho || "Not given")}</div>
          <div><strong>Needs help now:</strong> ${escapeHtml(helpLabel)}</div>
          <div><strong>Emergency number:</strong> ${escapeHtml(emergencyNumber)}</div>
        </div>
        <div class="fr-section">
          <div class="fr-section-title">What happened</div>
          <p>${escapeHtml(what || "Not stated")}</p>
        </div>
        <div class="fr-section">
          <div class="fr-section-title">Statement</div>
          <p>This is a child report generated in RECOVS so a grown-up, helper, teacher, institution, or authority can review what happened.</p>
        </div>
      </div>
      <div class="tool-row">
        <button class="pdf-btn" id="downloadChildReportBtn" type="button">Download report</button>
        <button class="share-btn" id="copyChildReportBtn" type="button">Copy report</button>
      </div>
    </div>
  `;

  const plainText = [
    "RECOVS Child Report",
    `Evaluation ID: ${evalId}`,
    `Timestamp: ${now.toISOString()}`,
    `Name: ${name || "Not given"}`,
    `Age: ${age || "Not given"}`,
    `Where: ${where || "Not given"}`,
    `Who is with you: ${withWho || "Not given"}`,
    `Needs help now: ${helpLabel}`,
    `Emergency number: ${emergencyNumber}`,
    `What happened: ${what || "Not stated"}`
  ].join("\n");

  $("downloadChildReportBtn").addEventListener("click", () => {
    const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><title>${escapeHtml(evalId)}</title><style>
      body{font-family:Georgia,serif;padding:40px;max-width:760px;margin:0 auto;color:#101316}
      h1{margin-bottom:8px} .muted{color:#635b52;font-family:monospace;font-size:12px}
      .row{display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #ddd}
      .key{min-width:160px;font-family:monospace;font-size:12px;color:#635b52}
      p{line-height:1.6}
    </style></head><body>
      <div class="muted">RECOVS Child Report</div>
      <h1>Child report</h1>
      ${[
        ["Evaluation ID", evalId],
        ["Timestamp", now.toISOString()],
        ["Name", name || "Not given"],
        ["Age", age || "Not given"],
        ["Where", where || "Not given"],
        ["Who is with you", withWho || "Not given"],
        ["Needs help now", helpLabel],
        ["Emergency number", emergencyNumber]
      ].map(([k,v]) => `<div class="row"><div class="key">${escapeHtml(k)}</div><div>${escapeHtml(v)}</div></div>`).join("")}
      <h2>What happened</h2>
      <p>${escapeHtml(what || "Not stated")}</p>
      <p>This is a child report generated in RECOVS so a grown-up, helper, teacher, institution, or authority can review what happened.</p>
    </body></html>`;
    downloadBlob(`${evalId}-child-report.html`, html, "text/html;charset=utf-8");
  });

  $("copyChildReportBtn").addEventListener("click", async () => {
    try{
      await navigator.clipboard.writeText(plainText);
      announce("Child report copied.");
    } catch(error){
      console.error("Copy failed", error);
      announce("Copy failed.");
    }
  });
}

function onCountryChange(){
  safeSetStorage(STORAGE_KEYS.country, $("countrySelect").value);
  updateCountryFlag();
}

function restoreCountry(){
  const saved = safeGetStorage(STORAGE_KEYS.country);
  if(saved){
    $("countrySelect").value = saved;
  }
}

function restoreActiveTab(){
  const saved = safeGetStorage(STORAGE_KEYS.activeTab) || "check";
  setActiveTab(saved);
}

function updateCountryFlag(){
  const val = $("countrySelect").value;
  const map = {
    AR: "Argentina",
    AU: "Australia",
    BR: "Brazil",
    CA: "Canada",
    FR: "France",
    DE: "Germany",
    IE: "Ireland",
    IT: "Italy",
    MX: "Mexico",
    PT: "Portugal",
    ES: "Spain",
    GB: "United Kingdom",
    US: "United States",
    DEFAULT: "International"
  };
  $("countryFlag").textContent = map[val] || "";
}

function renderSituationCards(){
  const grid = $("sitGrid");
  grid.innerHTML = "";

  SITUATIONS.forEach((situation) => {
    const card = document.createElement("button");
    card.className = "sit-card";
    card.type = "button";
    card.innerHTML = `
      <div class="sit-icon" aria-hidden="true">${situation.icon}</div>
      <div class="sit-label">${escapeHtml(situation.label)}</div>
      <div class="sit-sub">${escapeHtml(situation.sub)}</div>
    `;
    card.addEventListener("click", () => startSituation(situation.id));
    grid.appendChild(card);
  });
}

function startSituation(id){
  currentSituation = SITUATIONS.find((item) => item.id === id);
  currentState = {};
  safeSetStorage(STORAGE_KEYS.lastSituation, id);

  $("qDomainLabel").textContent = currentSituation.label;
  showSection("sec-questions");
  renderQuestions();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showSection(sectionId){
  ["sec-home", "sec-questions", "sec-result"].forEach((id) => {
    $(id).classList.toggle("active", id === sectionId);
  });
}

function renderQuestions(){
  const wrap = $("questionsContainer");
  wrap.innerHTML = "";
  const total = currentSituation.questions.length;

  currentSituation.questions.forEach((question, index) => {
    const block = document.createElement("section");
    block.className = "question-block";
    block.setAttribute("aria-labelledby", `${question.id}-title`);

    let inputHtml = "";
    if(question.yn){
      inputHtml = `
        <div class="yn-row" role="group" aria-label="${escapeAttribute(question.text)}">
          <button class="yn-btn" type="button" data-val="yes" aria-pressed="false">Yes</button>
          <button class="yn-btn" type="button" data-val="no" aria-pressed="false">No</button>
        </div>
      `;
    }
    if(question.num){
      inputHtml = `
        <div class="num-row">
          <input class="num-input" type="number" min="0" step="1" inputmode="numeric" placeholder="Enter value" aria-label="${escapeAttribute(question.text)}" />
          <span class="num-unit">${escapeHtml(question.unit || "")}</span>
        </div>
      `;
    }

    block.innerHTML = `
      <div class="q-number">Question ${index + 1} / ${total}</div>
      <div class="q-text" id="${question.id}-title">${escapeHtml(question.text)}</div>
      ${question.sub ? `<div class="q-sub">${escapeHtml(question.sub)}</div>` : ""}
      ${inputHtml}
    `;
    wrap.appendChild(block);

    if(question.yn){
      block.querySelectorAll(".yn-btn").forEach((button) => {
        button.addEventListener("click", () => {
          block.querySelectorAll(".yn-btn").forEach((peer) => {
            peer.classList.remove("selected-yes", "selected-no");
            peer.setAttribute("aria-pressed", "false");
          });

          const choice = button.dataset.val;
          button.classList.add(choice === "yes" ? "selected-yes" : "selected-no");
          button.setAttribute("aria-pressed", "true");
          currentState[question.field] = question[choice];
          updateProgress();
        });
      });
    }

    if(question.num){
      const input = block.querySelector(".num-input");
      input.addEventListener("input", () => {
        const raw = Number(input.value);
        currentState[question.field] = Number.isFinite(raw) ? raw * (question.mult || 1) : "";
        updateProgress();
      });
    }
  });

  updateProgress();
}

function updateProgress(){
  const total = currentSituation.questions.length;
  const answered = currentSituation.questions.filter((question) => currentState[question.field] !== undefined && currentState[question.field] !== "").length;
  const percent = Math.round((answered / total) * 100);

  $("progressFill").style.width = `${percent}%`;
  $("progressText").textContent = `${percent}% complete`;
  $("progressCount").textContent = `${answered} / ${total} answered`;
  $("checkBtn").style.display = answered === total ? "block" : "none";
  $("questionHint").textContent = answered === total ? "All questions answered. You can now evaluate the situation." : "Answer every question to continue.";
}

function evalRule(rule, state){
  const value = state[rule.field];
  if(value === undefined || value === null || value === ""){
    return { passed: null, unknown: true, rule };
  }

  let passed = true;
  if("val" in rule && value !== rule.val) passed = false;
  if("min" in rule && (Number.isNaN(Number(value)) || Number(value) < rule.min)) passed = false;

  return { passed, unknown: false, rule };
}

function evaluate(domain, state){
  const results = [];

  GLOBAL_RULES.forEach((rule) => results.push(evalRule(rule, state)));
  (DOMAIN_RULES[domain] || []).forEach((rule) => results.push(evalRule(rule, state)));

  const criticalFailures = results.filter((result) => !result.passed && !result.unknown && (result.rule.weight === "critical" || result.rule.weight === "execution_gate"));
  const majorFailures = results.filter((result) => !result.passed && !result.unknown && result.rule.weight === "major");
  const gateFailures = results.filter((result) => !result.passed && !result.unknown && result.rule.weight === "execution_gate");
  const timeLeft = Number(state.time_remaining_seconds) || 0;

  let stateOut = "CONTINUE";
  if(criticalFailures.length){
    stateOut = gateFailures.length || timeLeft < 3600 ? "NON-EXECUTABLE" : "NON-ADMISSIBLE";
  } else if(majorFailures.length){
    stateOut = "DEGRADED";
  }

  return {
    state: stateOut,
    failed: [...criticalFailures, ...majorFailures],
    results,
    timeLeft
  };
}

function runCheck(){
  const result = evaluate(currentSituation.id, currentState);
  renderResult(currentSituation, currentState, result);
  showSection("sec-result");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderResult(situation, state, result){
  const text = RESULT_TEXT[result.state];
  const failLines = result.failed.map((item) => `${item.rule.id} - ${item.rule.plain}`);
  const recordData = buildFormalRecordData(situation, state, result);
  lastRecordData = recordData;
  saveEvaluationHistory({
    state: recordData.stateLabel,
    domain: situation.label,
    timestampUtc: recordData.timestampUtc
  });

  $("statusLive").textContent = `${text.displayLabel}. ${text.headline}`;

  $("resultContent").innerHTML = `
    <div class="result-shell">
      <div class="result-state ${escapeAttribute(result.state)}">
        <div class="result-label">${escapeHtml(text.displayLabel)}</div>
        <h2 class="result-headline" id="resultTitle">${escapeHtml(text.headline)}</h2>
        <p class="result-body">${escapeHtml(text.body)}</p>
      </div>

      <div class="result-action">
        <div class="result-action-label">Required action</div>
        <div class="result-action-text">${escapeHtml(text.action)}</div>
      </div>

      ${failLines.length ? `
        <div class="tool-card">
          <div class="result-fails-label">Conditions that failed</div>
          <div class="fail-list">
            ${failLines.map((line) => `<div class="fail-item">${escapeHtml(line)}</div>`).join("")}
          </div>
        </div>
      ` : ""}

      <div class="record-preview-card">
        <div class="fr-label">Formal record preview</div>
        <div class="fr-section-title" style="margin-top:8px;">Evaluation ID</div>
        <p>${escapeHtml(recordData.evalId)}</p>
        <div class="fr-section-title" style="margin-top:14px;">Timestamp (UTC)</div>
        <p>${escapeHtml(recordData.timestampUtc)}</p>
        <div class="fr-section-title" style="margin-top:8px;">Who must act now</div>
        <p>${escapeHtml(recordData.authority)}</p>
        <div class="fr-section-title" style="margin-top:14px;">Maximum response window</div>
        <p>${escapeHtml(recordData.responseWindow)}</p>
        <div class="fr-section-title" style="margin-top:14px;">If no action occurs in time</div>
        <p>${escapeHtml(recordData.nextEscalation)}</p>
      </div>

      ${renderSupportOrganisations(situation.id)}

      <div class="tool-card">
        <div class="result-meta-label">Institution Handoff</div>
        <p class="hero-body small">
          Send the website link, the one-line description, and the generated record to a responsible institution or advocate.
        </p>
        <div class="tool-row">
          <button class="share-btn" id="copyInstitutionPacketBtn" type="button">Copy institution packet</button>
          <button class="share-btn" id="copyWebsiteLinkBtn" type="button">Copy website link</button>
        </div>
      </div>

      <div class="tool-row">
        <button class="pdf-btn" id="downloadRecordBtn" type="button">Download Record</button>
        <button class="share-btn" id="copySummaryBtn" type="button">Copy summary</button>
        <button class="share-btn" id="downloadJsonBtn" type="button">Download JSON</button>
      </div>

      <button class="again-btn" id="againBtn" type="button">Start again</button>

      <div class="hero-note" style="margin-bottom:0;">
        Evaluated: ${escapeHtml(recordData.timestampUtc)} UTC
        <br />
        Domain: ${escapeHtml(situation.label)}
        <br />
        Framework DOI: doi.org/10.5281/zenodo.19583410
      </div>
    </div>
  `;

  $("downloadRecordBtn").addEventListener("click", async () => {
    await downloadFormalRecord(recordData);
  });
  $("copySummaryBtn").addEventListener("click", () => copySummary(recordData));
  $("copyInstitutionPacketBtn").addEventListener("click", () => copyInstitutionPacket(recordData));
  $("copyWebsiteLinkBtn").addEventListener("click", copyWebsiteLink);
  $("downloadJsonBtn").addEventListener("click", async () => {
    await downloadJson(recordData);
  });
  $("againBtn").addEventListener("click", goHome);
}

function renderSupportOrganisations(domain){
  const organisations = getCrisisOrgs(domain);
  if(!organisations.length) return "";

  return `
    <div class="tool-card">
      <div class="result-meta-label">Support Organisations</div>
      <div class="org-list">
        ${organisations.map((org) => `
          <div class="org-item">
            <div class="org-meta">
              <div class="org-name">${escapeHtml(org.name)}</div>
              <div class="org-note">${escapeHtml(org.note)}</div>
            </div>
            ${renderOrgContact(org)}
          </div>
        `).join("")}
      </div>
    </div>
  `;
}

function renderOrgContact(org){
  const safeContact = escapeHtml(org.contact);
  if(org.type === "phone"){
    const tel = org.contact.replace(/[^0-9+]/g, "");
    return `<a class="org-contact" href="tel:${escapeAttribute(tel)}">${safeContact}</a>`;
  }
  if(org.type === "link"){
    return `<a class="org-contact" href="${escapeAttribute(org.contact)}" target="_blank" rel="noopener">Open</a>`;
  }
  return `<span class="org-contact">${safeContact}</span>`;
}

function getSelectedCountryCode(){
  return $("countrySelect").value || "DEFAULT";
}

function getCrisisOrgs(domain){
  const country = CRISIS_ORGS[getSelectedCountryCode()] || CRISIS_ORGS.DEFAULT;
  return country[domain] || country.default || CRISIS_ORGS.DEFAULT.default || [];
}

function buildFormalRecordData(situation, state, result){
  const now = new Date();
  const evalId = buildEvaluationId(now);
  const date = now.toLocaleDateString("en-GB", { day: "2-digit", month: "long", year: "numeric" });
  const time = now.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || "Local";
  const country = $("countrySelect").options[$("countrySelect").selectedIndex]?.text || "Not stated";
  const statusMap = result.timeLeft <= 0 ? "EXPIRED" : result.timeLeft < 3600 ? "CRITICAL" : result.timeLeft < 14400 ? "REDUCED" : "ADEQUATE";
  const stateText = RESULT_TEXT[result.state];

  return {
    recordId: evalId,
    evalId,
    date,
    time,
    timezone,
    timestampUtc: now.toISOString(),
    country,
    domain: situation.label,
    state: result.state,
    stateLabel: stateText.displayLabel,
    headline: stateText.headline,
    body: stateText.body,
    requiredAction: stateText.action,
    timeStatus: statusMap,
    timeRemaining: result.timeLeft ? `${Math.max(1, Math.round(result.timeLeft / 3600))} hour(s)` : "Expired / not stated",
    summary: `A ${situation.label.toLowerCase()} was evaluated under present conditions. At the time of evaluation, ${stateText.body.toLowerCase()}`,
    authority: situation.authority,
    formAction: result.state === "CONTINUE"
      ? "Monitor and re-evaluate"
      : result.state === "DEGRADED"
      ? "Restore weakened conditions"
      : result.state === "NON-ADMISSIBLE"
      ? "Escalate and restore recoverable conditions"
      : "Immediate emergency escalation",
    responseWindow: result.timeLeft ? `${Math.max(1, Math.round(result.timeLeft / 3600))} hour(s)` : "Immediate",
    nextEscalation: result.state === "NON-EXECUTABLE"
      ? "Escalate immediately to emergency services or the highest available responsible authority."
      : "Escalate to the next responsible authority if no corrective action occurs within the response window.",
    failedConditions: result.failed.map((item) => ({
      code: item.rule.id,
      plain: item.rule.plain,
      observed: String(state[item.rule.field]),
      weight: item.rule.weight
    })),
    escalationChain: [
      situation.authority,
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
    verification: evalId.split("-").pop(),
    generatedAtIso: now.toISOString()
  };
}

function generateDirectRecord(){
  const reporter = $("fr-reporter").value.trim();
  const role = $("fr-role").value.trim();
  const institution = $("fr-institution").value.trim();
  const what = $("fr-what").value.trim();
  const subject = $("fr-subject").value.trim();

  if(!what){
    $("recordValidation").classList.remove("hidden");
    $("recordValidation").textContent = "Please describe what happened before generating a direct formal record.";
    $("fr-what").focus();
    return;
  }

  $("recordValidation").classList.add("hidden");
  $("recordValidation").textContent = "";

  const now = new Date();
  const evalId = buildEvaluationId(now);
  const record = {
    recordId: evalId,
    evalId,
    date: now.toLocaleDateString("en-GB", { day: "2-digit", month: "long", year: "numeric" }),
    time: now.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }),
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "Local",
    timestampUtc: now.toISOString(),
    country: $("countrySelect").options[$("countrySelect").selectedIndex]?.text || "Not stated",
    domain: "Direct formal record",
    state: "NON-ADMISSIBLE",
    stateLabel: "NON-ADMISSIBLE",
    headline: "Continuation under current conditions is not admissible.",
    body: "A contemporaneous formal record has been created for responsible review and escalation.",
    requiredAction: "Escalate now to a responsible authority and preserve this record.",
    timeStatus: "NOT STATED",
    timeRemaining: "Not stated",
    summary: what,
    authority: institution || "Responsible authority / institution",
    formAction: "Review, acknowledge, and act",
    responseWindow: "As soon as possible",
    nextEscalation: "Escalate to the next available authority if no acknowledgment or action occurs.",
    failedConditions: [
      {
        code: "DR-001",
        plain: "Reported interruption or denial condition recorded",
        observed: "Reported by user",
        weight: "critical"
      }
    ],
    escalationChain: [
      institution || "Primary institution or service",
      "Service lead / supervisor",
      "Independent authority / external reviewer",
      "Emergency or legal escalation if delay creates irrecoverable loss"
    ],
    subject: subject || "Not stated",
    role: role || "Not stated",
    institution: institution || "Not stated",
    reporter: reporter || "Not stated",
    notice: "This record preserves a contemporaneous statement for responsible review. If conditions are time-critical, escalation should not be delayed.",
    verification: evalId.split("-").pop(),
    generatedAtIso: now.toISOString()
  };

  lastRecordData = record;
  $("recordPreview").classList.remove("hidden");
  $("recordPreview").innerHTML = `
    <div class="formal-record">
      <div class="fr-header">
        <div class="fr-kicker">RECOVS FORMAL RECORD</div>
        <div class="fr-title">Direct formal record preview</div>
      </div>
      <div class="fr-grid">
        <div><strong>Evaluation ID:</strong> ${escapeHtml(record.evalId)}</div>
        <div><strong>Timestamp (UTC):</strong> ${escapeHtml(record.timestampUtc)}</div>
        <div><strong>Reporter:</strong> ${escapeHtml(record.reporter)}</div>
        <div><strong>Role:</strong> ${escapeHtml(record.role)}</div>
      </div>
      <div class="fr-section">
        <div class="fr-section-title">What happened</div>
        <p>${escapeHtml(what)}</p>
      </div>
      <div class="fr-section">
        <div class="fr-section-title">Institution / service involved</div>
        <p>${escapeHtml(record.institution)}</p>
      </div>
      <div class="tool-row">
        <button class="pdf-btn" id="downloadDirectRecordBtn" type="button">Download Record</button>
        <button class="share-btn" id="copyDirectSummaryBtn" type="button">Copy summary</button>
      </div>
    </div>
  `;

  $("downloadDirectRecordBtn").addEventListener("click", async () => {
    await downloadFormalRecord(record);
  });
  $("copyDirectSummaryBtn").addEventListener("click", () => copySummary(record));
}

async function downloadFormalRecord(data){
  try{
    const prepared = await prepareRecordWithHash(data);
    if(await generatePdfRecord(prepared)) return;
    downloadHtmlRecord(prepared);
  } catch(error){
    console.error("PDF generation failed", error);
    announce("PDF generation failed. Downloading HTML record instead.");
    downloadHtmlRecord(data);
  }
}

function downloadHtmlRecord(data){
  const failedHtml = data.failedConditions.map((item) => `
    <div class="fr-fail">
      <strong>${escapeHtml(item.code)} - ${escapeHtml(item.plain)}</strong><br />
      Observed state: ${escapeHtml(item.observed)}<br />
      Effect on admissibility: ${escapeHtml(item.weight)}
    </div>
  `).join("");

  const chainHtml = data.escalationChain.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  const stateClass = data.state === "CONTINUE"
    ? "continue"
    : data.state === "DEGRADED"
    ? "degraded"
    : data.state === "NON-ADMISSIBLE"
    ? "non-admissible"
    : "non-executable";

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>${escapeHtml(data.recordId)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@300;600;700&family=DM+Mono:wght@400;500&display=swap');
    *{box-sizing:border-box}
    body{font-family:'Fraunces',Georgia,serif;color:#101316;background:#fff;padding:32px;max-width:780px;margin:0 auto;line-height:1.6}
    .fr-header{border-bottom:2px solid #101316;padding-bottom:14px;margin-bottom:18px}
    .fr-kicker,.fr-section-title{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#635b52}
    .fr-title{font-size:28px;line-height:1.15;margin-top:8px}
    .fr-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px 18px;margin-bottom:18px}
    .fr-state-box{border:3px solid #101316;border-radius:16px;padding:18px;margin-bottom:18px}
    .fr-state-box.non-admissible{border-color:#b84031}
    .fr-state-box.non-executable{border-color:#6847b8}
    .fr-state-box.degraded{border-color:#b46a12}
    .fr-state-box.continue{border-color:#1f6d41}
    .fr-state-value{font-size:30px;line-height:1.05;margin:8px 0}
    .fr-action-value{font-size:18px;font-weight:700;margin:8px 0 12px}
    .fr-time-row{display:flex;gap:12px 20px;flex-wrap:wrap;font-family:'DM Mono',monospace;font-size:12px;color:#635b52}
    .fr-section{margin-bottom:18px}
    .fr-fail{border-left:4px solid #b84031;background:#f8f5f2;padding:12px 14px;margin-top:10px}
    .fr-footer{border-top:1px solid #cfc1b0;padding-top:14px;margin-top:18px;font-family:'DM Mono',monospace;font-size:12px;color:#635b52;line-height:1.7}
    ol{padding-left:20px}
    li+li{margin-top:6px}
    @media print{body{padding:18px}.fr-grid{grid-template-columns:1fr 1fr}}
    @media (max-width:640px){body{padding:18px}.fr-grid{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <div class="fr-header">
    <div class="fr-kicker">RECOVS FORMAL RECORD</div>
    <div class="fr-title">Recoverability Evaluation and Admissibility Determination</div>
  </div>

  <div class="fr-grid">
    <div><strong>Record ID:</strong> ${escapeHtml(data.recordId)}</div>
    <div><strong>Evaluation ID:</strong> ${escapeHtml(data.evalId)}</div>
    <div><strong>Date:</strong> ${escapeHtml(data.date)}</div>
    <div><strong>Time:</strong> ${escapeHtml(data.time)}</div>
    <div><strong>Timestamp (UTC):</strong> ${escapeHtml(data.timestampUtc || data.generatedAtIso || "")}</div>
    <div><strong>Country / Jurisdiction:</strong> ${escapeHtml(data.country)}</div>
    <div><strong>Domain:</strong> ${escapeHtml(data.domain)}</div>
    <div><strong>Document hash:</strong> ${escapeHtml(data.documentHash || "Not generated")}</div>
  </div>

  <div class="fr-state-box ${stateClass}">
    <div class="fr-kicker">State</div>
    <div class="fr-state-value">${escapeHtml(data.stateLabel)}</div>
    <div>${escapeHtml(data.headline)} ${escapeHtml(data.body)}</div>
    <div class="fr-kicker" style="margin-top:14px;">Required action</div>
    <div class="fr-action-value">${escapeHtml(data.requiredAction)}</div>
    <div class="fr-time-row">
      <div><strong>Time status:</strong> ${escapeHtml(data.timeStatus)}</div>
      <div><strong>Time remaining:</strong> ${escapeHtml(data.timeRemaining)}</div>
    </div>
  </div>

  <div class="fr-section">
    <div class="fr-section-title">Admissibility Condition</div>
    <p>A situation may continue only while recoverability can be established in time under real conditions. Where recoverability cannot be established, verified, interpreted, enforced, or executed within the available time before irreversible transition, continuation is non-admissible and execution does not occur.</p>
  </div>

  <div class="fr-section">
    <div class="fr-section-title">Situation Summary</div>
    <p>${escapeHtml(data.summary)}</p>
  </div>

  <div class="fr-section">
    <div class="fr-section-title">Formal Statement</div>
    <p>This record is generated under Recoverability-Constrained Systems and represents a formal admissibility evaluation.</p>
  </div>

  <div class="fr-section">
    <div class="fr-section-title">Failed Conditions Identified</div>
    ${failedHtml || "<p>No failed conditions recorded.</p>"}
  </div>

  <div class="fr-section">
    <div class="fr-section-title">Who Must Act Now</div>
    <p><strong>Primary responsible authority:</strong> ${escapeHtml(data.authority)}</p>
    <p><strong>Required form of action:</strong> ${escapeHtml(data.formAction)}</p>
    <p><strong>Maximum response window:</strong> ${escapeHtml(data.responseWindow)}</p>
    <p><strong>If no action occurs in time:</strong> ${escapeHtml(data.nextEscalation)}</p>
  </div>

  <div class="fr-section">
    <div class="fr-section-title">Escalation Chain</div>
    <ol>${chainHtml}</ol>
  </div>

  <div class="fr-section">
    <div class="fr-section-title">Immediate Notice</div>
    <p>${escapeHtml(data.notice)}</p>
  </div>

  <div class="fr-footer">
    Framework DOI: doi.org/10.5281/zenodo.19583410<br />
    Generated by: RECOVS<br />
    Evaluation hash: ${escapeHtml(data.documentHash || "Not generated")}<br />
    This record evaluates recoverability only. It does not make or enforce clinical, legal, financial, or operational decisions.
  </div>
</body>
</html>`;

  const popup = window.open("", "_blank", "noopener,noreferrer");
  if(popup){
    popup.document.open();
    popup.document.write(html);
    popup.document.close();
    popup.focus();
    setTimeout(() => popup.print(), 350);
    return;
  }

  downloadBlob(`${data.recordId}.html`, html, "text/html;charset=utf-8");
}

async function downloadJson(data){
  const prepared = await prepareRecordWithHash(data);
  downloadBlob(`${data.recordId}.json`, JSON.stringify(prepared, null, 2), "application/json;charset=utf-8");
}

function downloadBlob(filename, text, type){
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function copySummary(record){
  const prepared = record.documentHash ? record : await prepareRecordWithHash(record);
  const text = [
    `RECOVS ${prepared.stateLabel}`,
    `Domain: ${prepared.domain}`,
    `Timestamp (UTC): ${prepared.timestampUtc}`,
    `Country: ${prepared.country}`,
    `Required action: ${prepared.requiredAction}`,
    `Authority: ${prepared.authority}`,
    `Evaluation ID: ${prepared.evalId}`,
    `Hash: ${prepared.documentHash}`
  ].join("\n");

  try{
    await navigator.clipboard.writeText(text);
    announce("Summary copied to clipboard.");
  } catch(error){
    announce("Copy failed. You can use the downloaded record instead.");
  }
}

async function copyInstitutionLine(){
  const line = "This system determines whether continuation is admissible under real-time recoverability constraints and generates a formal record.";
  try{
    await navigator.clipboard.writeText(line);
    announce("Institution line copied to clipboard.");
  } catch(error){
    announce("Copy failed.");
  }
}

async function copyWebsiteLink(){
  const url = window.location.href;
  try{
    await navigator.clipboard.writeText(url);
    announce("Website link copied to clipboard.");
  } catch(error){
    announce("Copy failed.");
  }
}

async function copyInstitutionPacket(record){
  const prepared = record.documentHash ? record : await prepareRecordWithHash(record);
  const packet = [
    window.location.href,
    "",
    "This system determines whether continuation is admissible under real-time recoverability constraints and generates a formal record.",
    "",
    `Evaluation ID: ${prepared.evalId}`,
    `State: ${prepared.stateLabel}`,
    `Required action: ${prepared.requiredAction}`,
    `Timestamp (UTC): ${prepared.timestampUtc}`,
    `Hash: ${prepared.documentHash}`
  ].join("\n");

  try{
    await navigator.clipboard.writeText(packet);
    announce("Institution packet copied to clipboard.");
  } catch(error){
    announce("Copy failed.");
  }
}

async function downloadExamplePdf(){
  const exampleRecord = await prepareRecordWithHash({
    recordId: "RECOVS-2026-04-21-8F3K2",
    evalId: "RECOVS-2026-04-21-8F3K2",
    date: "21 April 2026",
    time: "14:25",
    timezone: "UTC",
    timestampUtc: "2026-04-21T14:25:00.000Z",
    country: "Example / International",
    domain: "Healthcare problem",
    state: "NON-ADMISSIBLE",
    stateLabel: "NON-ADMISSIBLE",
    headline: "Continuation under current conditions is not admissible.",
    body: "Critical recovery conditions are not in place under present operating conditions.",
    requiredAction: "Escalate immediately to the responsible clinician, transport coordinator, or emergency authority.",
    timeStatus: "REDUCED",
    timeRemaining: "2 hour(s)",
    summary: "A patient transfer and treatment pathway was evaluated under present conditions. Transport continuity and responsible clinical reachability were not fully established in time.",
    authority: "Responsible clinician, hospital operations lead, emergency transport authority",
    formAction: "Escalate and restore recoverable conditions",
    responseWindow: "2 hour(s)",
    nextEscalation: "Escalate to emergency command or independent authority if corrective action does not occur inside the response window.",
    failedConditions: [
      {
        code: "HC-003",
        plain: "Your carer or support person is not available",
        observed: "false",
        weight: "critical"
      },
      {
        code: "GI-004",
        plain: "There is no backup option or alternative path",
        observed: "false",
        weight: "major"
      }
    ],
    escalationChain: [
      "Responsible clinician or service lead",
      "Hospital operations or transfer escalation lead",
      "Emergency transport or alternate receiving facility",
      "Independent regulator, public authority, or emergency escalation"
    ],
    subject: "Example institutional case",
    role: "Demonstration record",
    institution: "RECOVS Example",
    notice: "This example illustrates a formal admissibility record intended for institutional review and response.",
    verification: "8F3K2",
    generatedAtIso: "2026-04-21T14:25:00.000Z"
  });

  const generated = await generatePdfRecord(exampleRecord, {
    filename: "RECOVS-example-record.pdf"
  });

  if(!generated){
    downloadHtmlRecord(exampleRecord);
  }
}

async function prepareRecordWithHash(data){
  if(data.documentHash) return data;
  const clone = typeof structuredClone === "function"
    ? structuredClone(data)
    : JSON.parse(JSON.stringify(data));
  clone.documentHash = await hashEvaluation(clone);
  return clone;
}

async function hashEvaluation(data){
  if(!(crypto && crypto.subtle)){
    return simpleHash(JSON.stringify(sortKeys(data)));
  }
  const encoder = new TextEncoder();
  const payload = JSON.stringify(sortKeys(data));
  const digest = await crypto.subtle.digest("SHA-256", encoder.encode(payload));
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function sortKeys(value){
  if(Array.isArray(value)){
    return value.map(sortKeys);
  }
  if(value && typeof value === "object"){
    return Object.keys(value).sort().reduce((accumulator, key) => {
      accumulator[key] = sortKeys(value[key]);
      return accumulator;
    }, {});
  }
  return value;
}

function simpleHash(input){
  let hash = 2166136261;
  for(let index = 0; index < input.length; index += 1){
    hash ^= input.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return `fnv1a-${(hash >>> 0).toString(16).padStart(8, "0")}`;
}

async function generatePdfRecord(data, options = {}){
  const jsPdfApi = window.jspdf && window.jspdf.jsPDF;
  if(!jsPdfApi) return false;

  const doc = new jsPdfApi({ unit: "pt", format: "a4" });
  doc.setDocumentProperties({
    title: data.evalId,
    subject: "Formal admissibility evaluation",
    author: "RECOVS",
    keywords: "RECOVS, recoverability, admissibility, evidence",
    creator: "RECOVS"
  });
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 54;
  const contentWidth = pageWidth - margin * 2;
  let cursorY = margin;

  const colors = {
    ink: [16, 19, 22],
    muted: [99, 91, 82],
    line: [207, 193, 176],
    paper: [251, 248, 243],
    accent: data.state === "CONTINUE"
      ? [31, 109, 65]
      : data.state === "DEGRADED"
      ? [180, 106, 18]
      : data.state === "NON-ADMISSIBLE"
      ? [184, 64, 49]
      : [104, 71, 184]
  };

  const ensureSpace = (spaceNeeded) => {
    if(cursorY + spaceNeeded <= pageHeight - margin) return;
    doc.addPage();
    cursorY = margin;
  };

  const drawWrappedText = (text, x, y, width, options = {}) => {
    const lines = doc.splitTextToSize(text, width);
    doc.setFont(options.font || "times", options.style || "normal");
    doc.setFontSize(options.size || 11);
    doc.setTextColor(...(options.color || colors.ink));
    doc.text(lines, x, y, { lineHeightFactor: options.lineHeight || 1.45 });
    return lines.length * ((options.size || 11) * (options.lineHeight || 1.45));
  };

  const drawLabelValue = (label, value) => {
    ensureSpace(34);
    doc.setFont("courier", "normal");
    doc.setFontSize(9);
    doc.setTextColor(...colors.muted);
    doc.text(label.toUpperCase(), margin, cursorY);
    cursorY += 12;
    cursorY += drawWrappedText(value, margin, cursorY, contentWidth, { size: 11 });
    cursorY += 8;
  };

  doc.setFillColor(...colors.ink);
  doc.rect(margin, cursorY, contentWidth, 76, "F");
  doc.setTextColor(255, 255, 255);
  doc.setFont("courier", "normal");
  doc.setFontSize(10);
  doc.text("RECOVS FORMAL RECORD", margin + 18, cursorY + 20);
  doc.setFont("times", "bold");
  doc.setFontSize(22);
  doc.text("Formal Admissibility Evaluation", margin + 18, cursorY + 46);
  doc.setFont("times", "normal");
  doc.setFontSize(11);
  doc.text("Recoverability-Constrained Systems", margin + 18, cursorY + 64);
  cursorY += 98;

  doc.setDrawColor(...colors.line);
  doc.setFillColor(...colors.paper);
  doc.roundedRect(margin, cursorY, contentWidth, 110, 10, 10, "FD");
  doc.setTextColor(...colors.ink);
  doc.setFont("courier", "normal");
  doc.setFontSize(9);
  doc.text("EVALUATION OVERVIEW", margin + 18, cursorY + 18);
  doc.setFont("times", "bold");
  doc.setFontSize(24);
  doc.text(data.stateLabel, margin + 18, cursorY + 46);
  doc.setFont("times", "normal");
  doc.setFontSize(11);
  doc.text(`Evaluation ID: ${data.evalId}`, margin + 18, cursorY + 68);
  doc.text(`Timestamp (UTC): ${data.timestampUtc}`, margin + 18, cursorY + 84);
  doc.text(`Domain: ${data.domain}`, pageWidth / 2, cursorY + 68);
  doc.text(`Time window remaining: ${data.timeRemaining}`, pageWidth / 2, cursorY + 84);
  cursorY += 132;

  ensureSpace(88);
  doc.setFillColor(...colors.accent);
  doc.roundedRect(margin, cursorY, contentWidth, 78, 12, 12, "F");
  doc.setTextColor(255, 255, 255);
  doc.setFont("courier", "normal");
  doc.setFontSize(9);
  doc.text("REQUIRED ACTION", margin + 18, cursorY + 18);
  doc.setFont("times", "bold");
  doc.setFontSize(15);
  const actionLines = doc.splitTextToSize(data.requiredAction, contentWidth - 36);
  doc.text(actionLines, margin + 18, cursorY + 42, { lineHeightFactor: 1.35 });
  cursorY += 98;

  doc.setTextColor(...colors.ink);
  doc.setFont("courier", "normal");
  doc.setFontSize(9);
  doc.text("FORMAL STATEMENT", margin, cursorY);
  cursorY += 14;
  cursorY += drawWrappedText(
    "This record is generated under Recoverability-Constrained Systems and represents a formal admissibility evaluation.",
    margin,
    cursorY,
    contentWidth,
    { size: 12 }
  );
  cursorY += 12;

  drawLabelValue("Headline", data.headline);
  drawLabelValue("Summary", data.summary);
  drawLabelValue("Responsible authority", data.authority);
  drawLabelValue("Next escalation", data.nextEscalation);

  ensureSpace(60);
  doc.setFont("courier", "normal");
  doc.setFontSize(9);
  doc.setTextColor(...colors.muted);
  doc.text("FAILED CONDITIONS", margin, cursorY);
  cursorY += 14;
  if(data.failedConditions.length){
    data.failedConditions.forEach((item) => {
      const blockText = `${item.code} - ${item.plain}`;
      const height = doc.splitTextToSize(blockText, contentWidth - 28).length * 15 + 16;
      ensureSpace(height + 8);
      doc.setFillColor(248, 245, 242);
      doc.setDrawColor(...colors.line);
      doc.roundedRect(margin, cursorY, contentWidth, height, 8, 8, "FD");
      doc.setDrawColor(...colors.accent);
      doc.line(margin + 8, cursorY + 8, margin + 8, cursorY + height - 8);
      doc.setTextColor(...colors.ink);
      doc.setFont("times", "normal");
      doc.setFontSize(11);
      doc.text(doc.splitTextToSize(blockText, contentWidth - 28), margin + 18, cursorY + 20, { lineHeightFactor: 1.35 });
      cursorY += height + 10;
    });
  } else {
    cursorY += drawWrappedText("No failed conditions recorded.", margin, cursorY, contentWidth, { size: 11 });
    cursorY += 8;
  }

  drawLabelValue("Document hash (SHA-256)", data.documentHash);
  drawLabelValue("DOI reference", "doi.org/10.5281/zenodo.19583410");

  ensureSpace(50);
  doc.setDrawColor(...colors.line);
  doc.line(margin, pageHeight - margin - 18, pageWidth - margin, pageHeight - margin - 18);
  doc.setFont("courier", "normal");
  doc.setFontSize(8);
  doc.setTextColor(...colors.muted);
  doc.text("RECOVS evidence record", margin, pageHeight - margin);
  doc.text("doi.org/10.5281/zenodo.19583410", pageWidth - margin, pageHeight - margin, { align: "right" });

  doc.save(options.filename || `${data.evalId}.pdf`);
  announce("PDF record downloaded.");
  return true;
}

function announce(message){
  $("statusLive").textContent = message;
}

function goHome(){
  showSection("sec-home");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function bindRecordDraftPersistence(){
  ["fr-reporter", "fr-role", "fr-institution", "fr-what", "fr-subject"].forEach((id) => {
    $(id).addEventListener("input", saveDraftRecord);
  });
}

function saveProfile(){
  const profile = {
    name: $("prof-name").value.trim(),
    dob: $("prof-dob").value,
    blood: $("prof-blood").value,
    meds: $("prof-meds").value.trim(),
    allergies: $("prof-allergies").value.trim(),
    ec1: $("prof-ec1").value.trim(),
    ec2: $("prof-ec2").value.trim(),
    role: $("prof-role").value.trim()
  };
  safeSetStorage(STORAGE_KEYS.profile, JSON.stringify(profile));
  $("profileStatus").textContent = "Profile saved on this device.";
  prefillFromProfile(profile);
  updateLockCardPreview();
}

function loadProfile(){
  const raw = safeGetStorage(STORAGE_KEYS.profile);
  if(!raw) return null;
  try{
    const profile = JSON.parse(raw);
    $("prof-name").value = profile.name || "";
    $("prof-dob").value = profile.dob || "";
    $("prof-blood").value = profile.blood || "";
    $("prof-meds").value = profile.meds || "";
    $("prof-allergies").value = profile.allergies || "";
    $("prof-ec1").value = profile.ec1 || "";
    $("prof-ec2").value = profile.ec2 || "";
    $("prof-role").value = profile.role || "";
    return profile;
  } catch(error){
    safeRemoveStorage(STORAGE_KEYS.profile);
    return null;
  }
}

function clearProfile(){
  safeRemoveStorage(STORAGE_KEYS.profile);
  ["prof-name", "prof-dob", "prof-blood", "prof-meds", "prof-allergies", "prof-ec1", "prof-ec2", "prof-role"].forEach((id) => {
    $(id).value = "";
  });
  $("profileStatus").textContent = "Profile cleared.";
}

function prefillFromProfile(profile){
  if(!profile) return;
  const copyIfEmpty = (id, value) => {
    if(value && !$(id).value) $(id).value = value;
  };

  copyIfEmpty("fr-reporter", profile.name);
  copyIfEmpty("fr-role", profile.role);
  copyIfEmpty("ls-name", profile.name);
  copyIfEmpty("ls-dob", profile.dob);
  copyIfEmpty("ls-blood", profile.blood);
  copyIfEmpty("ls-meds", profile.meds);
  copyIfEmpty("ls-allergies", profile.allergies);
  copyIfEmpty("ls-ec1", profile.ec1);
  copyIfEmpty("ls-ec2", profile.ec2);
  updateLockCardPreview();
}

function saveEvaluationHistory(entry){
  const raw = safeGetStorage(STORAGE_KEYS.history);
  let history = [];
  try{
    history = raw ? JSON.parse(raw) : [];
  } catch(error){
    history = [];
  }
  history.unshift(entry);
  safeSetStorage(STORAGE_KEYS.history, JSON.stringify(history.slice(0, 10)));
  renderHistory();
}

function renderHistory(){
  const raw = safeGetStorage(STORAGE_KEYS.history);
  let history = [];
  try{
    history = raw ? JSON.parse(raw) : [];
  } catch(error){
    history = [];
  }

  const colors = {
    ADMISSIBLE: "var(--green)",
    DEGRADED: "var(--amber)",
    "NON-ADMISSIBLE": "var(--red)",
    "NON-EXECUTABLE": "var(--violet)"
  };

  if(!history.length){
    $("profileHistory").innerHTML = `<div class="history-sub">No evaluations yet.</div>`;
    return;
  }

  $("profileHistory").innerHTML = `
    <div class="history-list">
      ${history.map((item) => `
        <div class="history-item">
          <div class="history-dot" style="background:${colors[item.state] || "var(--muted)"};"></div>
          <div class="history-main">
            <div class="history-title">${escapeHtml(item.state)}</div>
            <div class="history-sub">${escapeHtml(item.domain)} · ${escapeHtml(new Date(item.timestampUtc).toLocaleString("en-GB"))}</div>
          </div>
        </div>
      `).join("")}
    </div>
  `;
}

function saveTrustedContact(){
  const trusted = {
    name: $("tc-name").value.trim(),
    email: $("tc-email").value.trim(),
    phone: $("tc-phone").value.trim(),
    message: $("tc-message").value.trim()
  };
  safeSetStorage(STORAGE_KEYS.trusted, JSON.stringify(trusted));
  $("trustedStatus").textContent = "Trusted contact saved.";
}

function loadTrustedContact(){
  const raw = safeGetStorage(STORAGE_KEYS.trusted);
  if(!raw) return null;
  try{
    const trusted = JSON.parse(raw);
    $("tc-name").value = trusted.name || "";
    $("tc-email").value = trusted.email || "";
    $("tc-phone").value = trusted.phone || "";
    $("tc-message").value = trusted.message || "";
    return trusted;
  } catch(error){
    safeRemoveStorage(STORAGE_KEYS.trusted);
    return null;
  }
}

function buildTrustedMessage(){
  const trusted = loadTrustedContact();
  const profile = loadProfile();
  return (trusted && trusted.message) || `${profile?.name || "I"} may need urgent help. Please contact me as soon as possible.`;
}

function sendEmailAlert(){
  const trusted = loadTrustedContact();
  if(!trusted?.email){
    $("trustedStatus").textContent = "Add an email first.";
    return;
  }
  const subject = encodeURIComponent("RECOVS alert");
  const body = encodeURIComponent(buildTrustedMessage());
  window.location.href = `mailto:${trusted.email}?subject=${subject}&body=${body}`;
}

function sendSmsAlert(){
  const trusted = loadTrustedContact();
  if(!trusted?.phone){
    $("trustedStatus").textContent = "Add a phone number first.";
    return;
  }
  const body = encodeURIComponent(buildTrustedMessage());
  window.location.href = `sms:${trusted.phone}?body=${body}`;
}

function addGroupMember(){
  const name = $("grp-name").value.trim();
  const domain = $("grp-domain").value;
  const state = $("grp-state").value;
  if(!name || !state) return;

  groupMembers.push({ name, domain, state });
  $("grp-name").value = "";
  $("grp-domain").value = "";
  $("grp-state").value = "";
  renderGroupSummary();
}

function renderGroupSummary(){
  const colors = {
    CONTINUE: "var(--green)",
    DEGRADED: "var(--amber)",
    "NON-ADMISSIBLE": "var(--red)",
    "NON-EXECUTABLE": "var(--violet)"
  };
  const labels = {
    CONTINUE: "Admissible",
    DEGRADED: "Degraded",
    "NON-ADMISSIBLE": "Non-admissible",
    "NON-EXECUTABLE": "Non-executable"
  };
  const counts = {
    CONTINUE: 0,
    DEGRADED: 0,
    "NON-ADMISSIBLE": 0,
    "NON-EXECUTABLE": 0
  };
  groupMembers.forEach((member) => {
    counts[member.state] += 1;
  });

  $("groupSummary").innerHTML = `
    <div class="summary-grid">
      ${Object.entries(counts).map(([key, value]) => `
        <div class="summary-cell">
          <div class="summary-value" style="color:${colors[key]};">${value}</div>
          <div class="summary-label">${labels[key]}</div>
        </div>
      `).join("")}
    </div>
  `;

  if(!groupMembers.length){
    $("groupList").innerHTML = `<div class="history-sub">No group members added yet.</div>`;
    return;
  }

  $("groupList").innerHTML = `
    <div class="group-list">
      ${groupMembers.map((member, index) => `
        <div class="group-item">
          <div class="group-dot" style="background:${colors[member.state]};"></div>
          <div class="group-main">
            <div class="group-title">${escapeHtml(member.name)}</div>
            <div class="group-sub">${escapeHtml(member.domain || "Unspecified domain")}</div>
          </div>
          <div class="group-badge" style="color:${colors[member.state]};">${escapeHtml(labels[member.state])}</div>
          <button class="mini-btn" type="button" data-remove-group="${index}">Remove</button>
        </div>
      `).join("")}
    </div>
  `;

  document.querySelectorAll("[data-remove-group]").forEach((button) => {
    button.addEventListener("click", () => {
      groupMembers.splice(Number(button.dataset.removeGroup), 1);
      renderGroupSummary();
    });
  });
}

function downloadGroupReport(){
  if(!groupMembers.length) return;
  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><title>RECOVS Group Report</title><style>
    body{font-family:Georgia,serif;padding:40px;max-width:760px;margin:0 auto;color:#101316}
    h1{margin-bottom:10px} table{width:100%;border-collapse:collapse;margin-top:20px}
    th,td{padding:10px 12px;border-bottom:1px solid #ddd;text-align:left}
    th{font-family:monospace;font-size:12px;text-transform:uppercase;color:#635b52}
  </style></head><body>
    <h1>RECOVS Group Report</h1>
    <p>Generated ${new Date().toISOString()}</p>
    <table><tr><th>Name</th><th>Domain</th><th>State</th></tr>
    ${groupMembers.map((member) => `<tr><td>${escapeHtml(member.name)}</td><td>${escapeHtml(member.domain || "")}</td><td>${escapeHtml(member.state)}</td></tr>`).join("")}
    </table>
  </body></html>`;
  downloadBlob("recovs-group-report.html", html, "text/html;charset=utf-8");
}

function updateLockCardPreview(){
  $("lc-name").textContent = $("ls-name").value || "Your name";
  $("lc-dob").textContent = $("ls-dob").value ? `DOB: ${$("ls-dob").value}` : "";
  $("lc-blood").textContent = $("ls-blood").value || "-";
  $("lc-meds").textContent = $("ls-meds").value || "-";
  $("lc-allergies").textContent = $("ls-allergies").value || "-";
  $("lc-ec1").textContent = $("ls-ec1").value || "-";
  $("lc-ec2").textContent = $("ls-ec2").value || "";
  $("lc-note").textContent = $("ls-note").value || "";
}

function downloadLockCard(){
  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><title>RECOVS Lock Card</title><style>
    body{background:#000;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}
    .card{background:#101316;color:#fff;border-radius:24px;padding:32px 24px;max-width:360px;width:100%;font-family:monospace}
    .label{font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.5;margin-bottom:16px}
    .name{font-size:26px;margin-bottom:4px}.sub{font-size:11px;opacity:.6;margin-bottom:18px}
    .block{margin-top:14px}.mini{font-size:9px;opacity:.45;text-transform:uppercase;margin-bottom:4px}
  </style></head><body><div class="card">
    <div class="label">Emergency Medical Information</div>
    <div class="name">${escapeHtml($("ls-name").value || "Your name")}</div>
    <div class="sub">${escapeHtml($("ls-dob").value ? `DOB: ${$("ls-dob").value}` : "")}</div>
    <div class="block"><div class="mini">Blood type</div><div>${escapeHtml($("ls-blood").value || "-")}</div></div>
    <div class="block"><div class="mini">Allergies</div><div>${escapeHtml($("ls-allergies").value || "-")}</div></div>
    <div class="block"><div class="mini">Critical medications</div><div>${escapeHtml($("ls-meds").value || "-")}</div></div>
    <div class="block"><div class="mini">Emergency contacts</div><div>${escapeHtml($("ls-ec1").value || "-")}</div><div>${escapeHtml($("ls-ec2").value || "")}</div></div>
    <div class="block"><div class="mini">Additional note</div><div>${escapeHtml($("ls-note").value || "")}</div></div>
  </div></body></html>`;
  downloadBlob("recovs-lock-card.html", html, "text/html;charset=utf-8");
}

function generateBehalfRecord(){
  const reporter = $("beh-reporter").value.trim();
  const subject = $("beh-subject").value.trim();
  const location = $("beh-location").value.trim();
  const observed = $("beh-state").value.trim();
  const risk = $("beh-risk").value.trim();
  const recovery = $("beh-recovery").value;
  const medical = $("beh-medical").value.trim();
  const action = $("beh-action").value.trim();
  const present = $("beh-present").value.trim();
  if(!observed) return;

  const now = new Date();
  const record = {
    recordId: buildEvaluationId(now),
    evalId: buildEvaluationId(now),
    timestampUtc: now.toISOString(),
    reporter,
    subject,
    location,
    observed,
    risk,
    recovery,
    medical,
    action,
    present
  };

  $("behalfPreview").classList.remove("hidden");
  $("behalfPreview").innerHTML = `
    <div class="formal-record">
      <div class="fr-header">
        <div class="fr-kicker">RECOVS FORMAL RECORD</div>
        <div class="fr-title">On-behalf record preview</div>
      </div>
      <div class="fr-grid">
        <div><strong>Evaluation ID:</strong> ${escapeHtml(record.evalId)}</div>
        <div><strong>Timestamp (UTC):</strong> ${escapeHtml(record.timestampUtc)}</div>
        <div><strong>Recorded by:</strong> ${escapeHtml(reporter || "Not stated")}</div>
        <div><strong>Person:</strong> ${escapeHtml(subject || "Not stated")}</div>
      </div>
      <div class="fr-section"><div class="fr-section-title">Observed state</div><p>${escapeHtml(observed)}</p></div>
      <div class="fr-section"><div class="fr-section-title">Immediate risk</div><p>${escapeHtml(risk || "Not stated")}</p></div>
      <div class="tool-row">
        <button class="pdf-btn" id="downloadBehalfBtn" type="button">Download record</button>
      </div>
    </div>
  `;

  $("downloadBehalfBtn").addEventListener("click", () => {
    const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><title>${escapeHtml(record.evalId)}</title><style>
      body{font-family:Georgia,serif;padding:40px;max-width:760px;margin:0 auto;color:#101316}
      h1{margin-bottom:10px}.row{display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #ddd}.key{min-width:140px;font-family:monospace;font-size:12px;color:#635b52}
    </style></head><body><h1>RECOVS On-Behalf Record</h1>
    ${[
      ["Evaluation ID", record.evalId],
      ["Timestamp (UTC)", record.timestampUtc],
      ["Recorded by", reporter || "Not stated"],
      ["Person", subject || "Not stated"],
      ["Location", location || "Not stated"],
      ["Observed state", observed],
      ["Immediate risk", risk || "Not stated"],
      ["Recovery path", recovery || "Not stated"],
      ["Medical information", medical || "Not stated"],
      ["Action taken", action || "Not stated"],
      ["Who else is present", present || "Not stated"]
    ].map(([k,v]) => `<div class="row"><div class="key">${escapeHtml(k)}</div><div>${escapeHtml(v)}</div></div>`).join("")}
    </body></html>`;
    downloadBlob(`${record.evalId}-behalf.html`, html, "text/html;charset=utf-8");
  });
}

function generateWitnessRecord(){
  const name = $("wit-name").value.trim();
  const contact = $("wit-contact").value.trim();
  const when = $("wit-when").value;
  const where = $("wit-where").value.trim();
  const persons = $("wit-persons").value.trim();
  const what = $("wit-what").value.trim();
  const context = $("wit-context").value.trim();
  const followup = $("wit-followup").value;
  if(!what) return;

  const now = new Date();
  const record = {
    recordId: buildEvaluationId(now),
    evalId: buildEvaluationId(now),
    timestampUtc: now.toISOString(),
    name,
    contact,
    when,
    where,
    persons,
    what,
    context,
    followup
  };

  $("witnessPreview").classList.remove("hidden");
  $("witnessPreview").innerHTML = `
    <div class="formal-record">
      <div class="fr-header">
        <div class="fr-kicker">RECOVS FORMAL RECORD</div>
        <div class="fr-title">Witness record preview</div>
      </div>
      <div class="fr-grid">
        <div><strong>Evaluation ID:</strong> ${escapeHtml(record.evalId)}</div>
        <div><strong>Timestamp (UTC):</strong> ${escapeHtml(record.timestampUtc)}</div>
        <div><strong>Witness:</strong> ${escapeHtml(name || "Anonymous")}</div>
        <div><strong>Occurred at:</strong> ${escapeHtml(when || "Not stated")}</div>
      </div>
      <div class="fr-section"><div class="fr-section-title">What was witnessed</div><p>${escapeHtml(what)}</p></div>
      <div class="tool-row">
        <button class="pdf-btn" id="downloadWitnessBtn" type="button">Download record</button>
      </div>
    </div>
  `;

  $("downloadWitnessBtn").addEventListener("click", () => {
    const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><title>${escapeHtml(record.evalId)}</title><style>
      body{font-family:Georgia,serif;padding:40px;max-width:760px;margin:0 auto;color:#101316}
      h1{margin-bottom:10px}.row{display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #ddd}.key{min-width:140px;font-family:monospace;font-size:12px;color:#635b52}
    </style></head><body><h1>RECOVS Witness Record</h1>
    ${[
      ["Evaluation ID", record.evalId],
      ["Timestamp (UTC)", record.timestampUtc],
      ["Witness", name || "Anonymous"],
      ["Contact", contact || "Not provided"],
      ["When", when || "Not stated"],
      ["Where", where || "Not stated"],
      ["Persons involved", persons || "Not stated"],
      ["What was witnessed", what],
      ["Context", context || "Not stated"],
      ["Available for follow-up", followup]
    ].map(([k,v]) => `<div class="row"><div class="key">${escapeHtml(k)}</div><div>${escapeHtml(v)}</div></div>`).join("")}
    </body></html>`;
    downloadBlob(`${record.evalId}-witness.html`, html, "text/html;charset=utf-8");
  });
}

function startCheckin(){
  const name = $("ci-name").value.trim();
  const ecName = $("ci-ec-name").value.trim();
  const ecContact = $("ci-ec-contact").value.trim();
  const message = $("ci-message").value.trim();
  const interval = Number($("ci-interval").value);
  if(!message) return;

  checkinData = { name, ecName, ecContact, message, interval };
  nextCheckin = Date.now() + interval * 1000;
  safeSetStorage(STORAGE_KEYS.checkin, JSON.stringify({ ...checkinData, nextCheckin }));
  $("checkinStatus").textContent = "Check-in started on this device.";
  renderCheckinActive();
  if(checkinTimer) clearInterval(checkinTimer);
  checkinTimer = setInterval(updateCheckinCountdown, 1000);
  updateCheckinCountdown();
}

function restoreCheckin(){
  const raw = safeGetStorage(STORAGE_KEYS.checkin);
  if(!raw) return;
  try{
    const saved = JSON.parse(raw);
    checkinData = saved;
    nextCheckin = saved.nextCheckin;
    $("ci-name").value = saved.name || "";
    $("ci-ec-name").value = saved.ecName || "";
    $("ci-ec-contact").value = saved.ecContact || "";
    $("ci-message").value = saved.message || "";
    $("ci-interval").value = String(saved.interval || 43200);
    renderCheckinActive();
    if(nextCheckin > Date.now()){
      if(checkinTimer) clearInterval(checkinTimer);
      checkinTimer = setInterval(updateCheckinCountdown, 1000);
      updateCheckinCountdown();
    }
  } catch(error){
    safeRemoveStorage(STORAGE_KEYS.checkin);
  }
}

function renderCheckinActive(){
  if(!checkinData){
    $("checkinActive").innerHTML = `<div class="history-sub">No active check-in.</div>`;
    return;
  }
  $("checkinActive").innerHTML = `
    <div class="formal-record">
      <div class="fr-section">
        <div class="fr-section-title">Countdown</div>
        <div class="fr-state-value" id="checkinCountdown">--</div>
      </div>
      <div class="fr-section">
        <div class="fr-section-title">If missed, show this</div>
        <p><strong>${escapeHtml(checkinData.name || "This person")}</strong> has not checked in. Contact ${escapeHtml(checkinData.ecName || "their emergency contact")} at ${escapeHtml(checkinData.ecContact || "the saved contact")}.</p>
        <p style="margin-top:8px;">${escapeHtml(checkinData.message)}</p>
      </div>
      <div class="tool-row">
        <button class="check-btn" id="confirmCheckinBtn" type="button">I am okay — check in now</button>
        <button class="again-btn" id="stopCheckinBtn" type="button">Stop check-in</button>
      </div>
    </div>
  `;
  $("confirmCheckinBtn").addEventListener("click", doCheckin);
  $("stopCheckinBtn").addEventListener("click", stopCheckin);
}

function updateCheckinCountdown(){
  if(!nextCheckin) return;
  const remaining = Math.max(0, nextCheckin - Date.now());
  const hours = Math.floor(remaining / 3600000);
  const minutes = Math.floor((remaining % 3600000) / 60000);
  const seconds = Math.floor((remaining % 60000) / 1000);
  const label = hours > 0 ? `${hours}h ${minutes}m` : minutes > 0 ? `${minutes}m ${seconds}s` : `${seconds}s`;
  const el = $("checkinCountdown");
  if(el) el.textContent = label;
  if(remaining === 0){
    if(el) el.textContent = "MISSED";
    $("checkinStatus").textContent = "Check-in overdue.";
    clearInterval(checkinTimer);
  }
}

function doCheckin(){
  if(!checkinData) return;
  nextCheckin = Date.now() + checkinData.interval * 1000;
  safeSetStorage(STORAGE_KEYS.checkin, JSON.stringify({ ...checkinData, nextCheckin }));
  $("checkinStatus").textContent = "Checked in successfully.";
  renderCheckinActive();
  if(checkinTimer) clearInterval(checkinTimer);
  checkinTimer = setInterval(updateCheckinCountdown, 1000);
  updateCheckinCountdown();
}

function stopCheckin(){
  if(checkinTimer) clearInterval(checkinTimer);
  checkinTimer = null;
  checkinData = null;
  nextCheckin = null;
  safeRemoveStorage(STORAGE_KEYS.checkin);
  $("checkinStatus").textContent = "Check-in stopped.";
  renderCheckinActive();
}

function saveDraftRecord(){
  const draft = {
    reporter: $("fr-reporter").value,
    role: $("fr-role").value,
    institution: $("fr-institution").value,
    what: $("fr-what").value,
    subject: $("fr-subject").value
  };
  safeSetStorage(STORAGE_KEYS.draftRecord, JSON.stringify(draft));
}

function restoreDraftRecord(){
  const raw = safeGetStorage(STORAGE_KEYS.draftRecord);
  if(!raw) return;

  try{
    const draft = JSON.parse(raw);
    $("fr-reporter").value = draft.reporter || "";
    $("fr-role").value = draft.role || "";
    $("fr-institution").value = draft.institution || "";
    $("fr-what").value = draft.what || "";
    $("fr-subject").value = draft.subject || "";
  } catch(error){
    safeRemoveStorage(STORAGE_KEYS.draftRecord);
  }
}

function makeCode(){
  if(window.crypto && typeof window.crypto.randomUUID === "function"){
    return window.crypto.randomUUID().replaceAll("-", "").slice(0, 5).toUpperCase();
  }
  return Math.random().toString(36).replace(/[^a-z0-9]/gi, "").slice(2, 7).toUpperCase();
}

function buildEvaluationId(date){
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  const day = String(date.getUTCDate()).padStart(2, "0");
  return `RECOVS-${year}-${month}-${day}-${makeCode()}`;
}

function escapeHtml(value){
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttribute(value){
  return escapeHtml(value).replaceAll("`", "&#96;");
}

function safeSetStorage(key, value){
  try{
    localStorage.setItem(key, value);
  } catch(error){
    return;
  }
}

function safeGetStorage(key){
  try{
    return localStorage.getItem(key);
  } catch(error){
    return null;
  }
}

function safeRemoveStorage(key){
  try{
    localStorage.removeItem(key);
  } catch(error){
    return;
  }
}

async function registerSW(){
  if(!("serviceWorker" in navigator)) return;
  try{
    await navigator.serviceWorker.register("sw.js");
  } catch(error){
    console.log("SW unavailable", error);
  }
}
