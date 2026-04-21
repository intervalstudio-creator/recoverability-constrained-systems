"""
Boundary — Plain-Language Case Builder

A person describes their situation in ordinary words.
The system translates it into a formal recoverability evaluation
that an institution cannot dismiss as anecdotal.

This is the language gap: the people most affected by non-admissible
continuity are usually the least able to articulate it formally.

This module bridges that gap.
"""

import re
from typing import Optional


# ─────────────────────────────────────────────
# Question Trees per Domain
# Guides a non-expert through their situation
# step by step, in plain language
# ─────────────────────────────────────────────

QUESTION_TREES = {
    "pharmacological": {
        "label": "Medication / prescription problem",
        "questions": [
            {
                "id": "q_supply",
                "text": "Do you have enough medication to last the next few days?",
                "yes_no": True,
                "maps_to": {"field": "supply_days_remaining", "yes_value": 7, "no_value": 0},
                "follow_up_if_no": "q_supply_days",
            },
            {
                "id": "q_supply_days",
                "text": "How many days of medication do you have left?",
                "numeric": True,
                "maps_to": {"field": "supply_days_remaining"},
            },
            {
                "id": "q_prescriber",
                "text": "Can you reach your doctor or prescriber right now if needed?",
                "yes_no": True,
                "maps_to": {"field": "prescriber_reachable", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_stop_risk",
                "text": "Would stopping this medication suddenly be dangerous? (For example: benzodiazepines, opioids, insulin, epilepsy medication, blood thinners)",
                "yes_no": True,
                "maps_to": {"field": "abrupt_stop_risk", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_pharmacy",
                "text": "Can you physically get to a pharmacy or have medication delivered?",
                "yes_no": True,
                "maps_to": {"field": "dispensing_accessible", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_taper",
                "text": "Does this medication need to be reduced gradually (tapered) rather than stopped?",
                "yes_no": True,
                "maps_to": {"field": "taper_required", "yes_value": True, "no_value": False},
                "follow_up_if_yes": "q_taper_plan",
            },
            {
                "id": "q_taper_plan",
                "text": "Is there a written taper plan from your doctor?",
                "yes_no": True,
                "maps_to": {"field": "taper_plan_exists", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_time_window",
                "text": "How many hours before this becomes an emergency if nothing changes?",
                "numeric": True,
                "maps_to": {"field": "time_remaining_seconds", "multiplier": 3600},
            },
            {
                "id": "q_human",
                "text": "Is there someone — a doctor, care coordinator, pharmacist, or emergency service — who you could contact right now and who could actually help?",
                "yes_no": True,
                "maps_to": {"field": "human_authority_reachable", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_fallback",
                "text": "Is there any alternative path — a different pharmacy, a walk-in clinic, an emergency prescription service?",
                "yes_no": True,
                "maps_to": {"field": "fallback_path_available", "yes_value": True, "no_value": False},
            },
        ],
    },

    "healthcare": {
        "label": "Healthcare / medical appointment problem",
        "questions": [
            {
                "id": "q_appointment",
                "text": "Have you missed or are you about to miss a critical medical appointment?",
                "yes_no": True,
                "maps_to": {"field": "critical_appointment_missed", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_transport",
                "text": "Do you have a way to get to the hospital or clinic if needed?",
                "yes_no": True,
                "maps_to": {"field": "transport_available", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_caregiver",
                "text": "Is your carer or support person available right now?",
                "yes_no": True,
                "maps_to": {"field": "caregiver_available", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_oxygen",
                "text": "Do you depend on oxygen at home?",
                "yes_no": True,
                "maps_to": {"field": "oxygen_dependent", "yes_value": True, "no_value": False},
                "follow_up_if_yes": "q_oxygen_supply",
            },
            {
                "id": "q_oxygen_supply",
                "text": "Has your oxygen supply been interrupted or is it about to run out?",
                "yes_no": True,
                "maps_to": {"field": "oxygen_interrupted", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_time_window",
                "text": "How many hours before this becomes a serious emergency?",
                "numeric": True,
                "maps_to": {"field": "time_remaining_seconds", "multiplier": 3600},
            },
            {
                "id": "q_human",
                "text": "Can you reach a doctor, nurse, or emergency service right now?",
                "yes_no": True,
                "maps_to": {"field": "human_authority_reachable", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_fallback",
                "text": "Is there any alternative — a different hospital, a home visit service, an emergency helpline?",
                "yes_no": True,
                "maps_to": {"field": "fallback_path_available", "yes_value": True, "no_value": False},
            },
        ],
    },

    "finance": {
        "label": "Bank / money / payment problem",
        "questions": [
            {
                "id": "q_bank",
                "text": "Is your bank account locked or frozen?",
                "yes_no": True,
                "maps_to": {"field": "bank_locked", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_payment",
                "text": "Are you unable to pay for something essential — rent, food, utilities, medication?",
                "yes_no": True,
                "maps_to": {"field": "essential_payment_blocked", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_income",
                "text": "Has your income or benefit payment stopped or been delayed?",
                "yes_no": True,
                "maps_to": {"field": "income_interrupted", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_time_window",
                "text": "How many hours before you face a serious consequence (eviction, missed medication, no food)?",
                "numeric": True,
                "maps_to": {"field": "time_remaining_seconds", "multiplier": 3600},
            },
            {
                "id": "q_human",
                "text": "Can you reach your bank, a financial adviser, or a welfare support service right now?",
                "yes_no": True,
                "maps_to": {"field": "human_authority_reachable", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_fallback",
                "text": "Is there an alternative — a different account, a family member who can help, a crisis fund?",
                "yes_no": True,
                "maps_to": {"field": "fallback_path_available", "yes_value": True, "no_value": False},
            },
        ],
    },

    "housing": {
        "label": "Housing / accommodation problem",
        "questions": [
            {
                "id": "q_eviction",
                "text": "Are you facing eviction or being forced to leave your home?",
                "yes_no": True,
                "maps_to": {"field": "eviction_imminent", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_utilities",
                "text": "Have your utilities (gas, electricity, water) been cut off?",
                "yes_no": True,
                "maps_to": {"field": "utilities_disconnected", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_habitable",
                "text": "Is your home currently unsafe or uninhabitable?",
                "yes_no": True,
                "maps_to": {"field": "habitability_failure", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_time_window",
                "text": "How many hours before you have to leave or this becomes a crisis?",
                "numeric": True,
                "maps_to": {"field": "time_remaining_seconds", "multiplier": 3600},
            },
            {
                "id": "q_human",
                "text": "Can you reach a housing officer, council, or emergency housing service right now?",
                "yes_no": True,
                "maps_to": {"field": "human_authority_reachable", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_fallback",
                "text": "Is there anywhere else you could go — family, a shelter, emergency accommodation?",
                "yes_no": True,
                "maps_to": {"field": "fallback_path_available", "yes_value": True, "no_value": False},
            },
        ],
    },

    "identity": {
        "label": "Identity / documents problem",
        "questions": [
            {
                "id": "q_id",
                "text": "Have you lost your identity documents (passport, driving licence, ID card)?",
                "yes_no": True,
                "maps_to": {"field": "id_document_available", "yes_value": False, "no_value": True},
            },
            {
                "id": "q_access",
                "text": "Are you locked out of essential accounts or services because of missing ID?",
                "yes_no": True,
                "maps_to": {"field": "access_recovery_available", "yes_value": False, "no_value": True},
            },
            {
                "id": "q_payroll",
                "text": "Is your ability to receive pay or benefits affected?",
                "yes_no": True,
                "maps_to": {"field": "payroll_identity_intact", "yes_value": False, "no_value": True},
            },
            {
                "id": "q_time_window",
                "text": "How many hours before this causes a serious problem?",
                "numeric": True,
                "maps_to": {"field": "time_remaining_seconds", "multiplier": 3600},
            },
            {
                "id": "q_human",
                "text": "Can you reach a government office, your employer, or an identity recovery service?",
                "yes_no": True,
                "maps_to": {"field": "human_authority_reachable", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_fallback",
                "text": "Is there any alternative way to prove your identity for now?",
                "yes_no": True,
                "maps_to": {"field": "fallback_path_available", "yes_value": True, "no_value": False},
            },
        ],
    },

    "disaster": {
        "label": "Emergency / disaster situation",
        "questions": [
            {
                "id": "q_window",
                "text": "Is there still time to evacuate or reach safety?",
                "yes_no": True,
                "maps_to": {"field": "evacuation_window_closed", "yes_value": False, "no_value": True},
            },
            {
                "id": "q_shelter",
                "text": "Have you been assigned to a shelter or safe location?",
                "yes_no": True,
                "maps_to": {"field": "shelter_assigned", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_comms",
                "text": "Have you lost the ability to communicate with emergency services or family?",
                "yes_no": True,
                "maps_to": {"field": "comms_collapsed", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_time_window",
                "text": "How many hours before the situation becomes irreversible?",
                "numeric": True,
                "maps_to": {"field": "time_remaining_seconds", "multiplier": 3600},
            },
            {
                "id": "q_human",
                "text": "Can you reach emergency services, a responder, or someone who can help right now?",
                "yes_no": True,
                "maps_to": {"field": "human_authority_reachable", "yes_value": True, "no_value": False},
            },
            {
                "id": "q_fallback",
                "text": "Is there a route or plan that still leads to safety?",
                "yes_no": True,
                "maps_to": {"field": "fallback_path_available", "yes_value": True, "no_value": False},
            },
        ],
    },
}

# Domain selector — shown first in the plain-language flow
DOMAIN_SELECTOR = [
    {"id": "pharmacological", "label": "Medication / prescription problem"},
    {"id": "healthcare",      "label": "Healthcare / medical appointment"},
    {"id": "finance",         "label": "Bank / money / payment problem"},
    {"id": "housing",         "label": "Housing / accommodation problem"},
    {"id": "identity",        "label": "Identity / documents problem"},
    {"id": "disaster",        "label": "Emergency / disaster situation"},
    {"id": "legal",           "label": "Legal / court / enforcement problem"},
    {"id": "labour",          "label": "Work / wages / unsafe conditions"},
    {"id": "infrastructure",  "label": "Power / internet / system failure"},
]


# ─────────────────────────────────────────────
# Answer Translator
# Converts plain-language answers to formal state dict
# ─────────────────────────────────────────────

def translate_answers_to_state(domain: str, answers: dict) -> dict:
    """
    Takes a dict of {question_id: answer} and translates to a
    formal recoverability state dict for the engine.
    """
    tree = QUESTION_TREES.get(domain)
    if not tree:
        return answers  # pass through if no translation available

    state = {}
    questions_by_id = {q["id"]: q for q in tree["questions"]}

    for q_id, answer in answers.items():
        q = questions_by_id.get(q_id)
        if not q:
            continue
        mapping = q.get("maps_to", {})
        field = mapping.get("field")
        if not field:
            continue

        if q.get("yes_no"):
            value = mapping.get("yes_value") if answer is True else mapping.get("no_value")
            state[field] = value
        elif q.get("numeric"):
            try:
                raw = float(answer)
                multiplier = mapping.get("multiplier", 1)
                state[field] = raw * multiplier
            except (ValueError, TypeError):
                pass

    # Add default recoverability conditions if time was provided
    if "time_remaining_seconds" in state:
        t = state["time_remaining_seconds"]
        # Derive recoverability conditions from answers
        state.setdefault("recovery_path_exists",                  state.get("fallback_path_available", False))
        state.setdefault("recovery_path_reachable",               state.get("human_authority_reachable", False))
        state.setdefault("failure_detectable_in_time",            True)  # they detected it — they're filling this in
        state.setdefault("response_possible_in_time",             t > 3600)
        state.setdefault("recovery_executable_in_time",           t > 7200)
        state.setdefault("no_irreversible_transition_before_recovery", t > 0)

    return state


def build_case_from_answers(domain: str, answers: dict, label: str = "") -> dict:
    """
    Build a complete case dict from plain-language answers,
    ready to pass directly to the evaluation engine.
    """
    state = translate_answers_to_state(domain, answers)
    return {
        "domain": domain,
        "label":  label or f"Plain-language case — {domain}",
        "state":  state,
    }


def get_question_tree(domain: str) -> Optional[dict]:
    return QUESTION_TREES.get(domain)


def get_domain_selector() -> list[dict]:
    return DOMAIN_SELECTOR


# ─────────────────────────────────────────────
# Plain-language result explainer
# Translates evaluation output back to plain language
# ─────────────────────────────────────────────

STATE_PLAIN_LANGUAGE = {
    "CONTINUE": {
        "headline": "Your situation appears manageable right now.",
        "explanation": "Based on what you have described, the key conditions for continuing safely appear to be in place. You should still monitor the situation and act if anything changes.",
        "action": "Monitor. Keep the situation under review. Contact your relevant authority if conditions change.",
        "colour": "green",
    },
    "DEGRADED": {
        "headline": "Your situation is weakened. Action is needed soon.",
        "explanation": "One or more important conditions are not fully in place. You are not yet in a crisis, but your safety margin has reduced. Act before it reduces further.",
        "action": "Act now to restore the weakened conditions. Do not wait.",
        "colour": "amber",
    },
    "NON-ADMISSIBLE": {
        "headline": "Your situation cannot continue as it is.",
        "explanation": "Based on what you have described, continuation is not safe. The conditions needed for a safe outcome are not in place. This must be escalated to someone who can help.",
        "action": "Do not continue without help. Contact a responsible authority immediately.",
        "colour": "red",
    },
    "NON-EXECUTABLE": {
        "headline": "This is a crisis. You need help right now.",
        "explanation": "Your situation cannot continue and time is running out — or the person who could help cannot be reached. This is an emergency. Do not wait.",
        "action": "Contact emergency services or your crisis support immediately. Do not delay.",
        "colour": "purple",
        "emergency": True,
    },
}


def explain_result_plain(evaluation_result: dict) -> dict:
    state = evaluation_result.get("boundary_state", "NON-ADMISSIBLE")
    explanation = STATE_PLAIN_LANGUAGE.get(state, STATE_PLAIN_LANGUAGE["NON-ADMISSIBLE"]).copy()

    # Add plain-language descriptions of what failed
    failed = evaluation_result.get("failed_conditions", [])
    plain_failures = []
    for f in failed:
        reason = f.get("reason", "")
        # Translate technical reason to plain language
        plain = reason \
            .replace("supply_days_remaining", "your medication supply") \
            .replace("prescriber_reachable", "your ability to reach your doctor") \
            .replace("abrupt_stop_risk", "the risk of stopping suddenly") \
            .replace("dispensing_accessible", "your access to a pharmacy") \
            .replace("taper_plan_exists", "your taper plan") \
            .replace("human_authority_reachable", "your ability to reach someone who can help") \
            .replace("fallback_path_available", "a backup option") \
            .replace("time_remaining_seconds", "the time remaining") \
            .replace("recovery_path_exists", "a way to recover") \
            .replace("bank_locked", "access to your bank") \
            .replace("essential_payment_blocked", "ability to pay for essentials") \
            .replace("eviction_imminent", "your housing security") \
            .replace("caregiver_available", "your carer being available") \
            .replace("oxygen_interrupted", "your oxygen supply") \
            .replace("True", "yes") \
            .replace("False", "no")
        plain_failures.append(plain)

    explanation["failed_conditions_plain"] = plain_failures
    explanation["domain"] = evaluation_result.get("domain", "")
    explanation["boundary_state"] = state
    return explanation
