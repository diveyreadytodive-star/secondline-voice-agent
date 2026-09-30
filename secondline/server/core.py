"""Pure SecondLine session configuration and rehearsal feedback.

Feedback is intentionally rule based. It surfaces literal phrases from a
fictional pressure exercise; it is not a fraud classifier.
"""

from __future__ import annotations

import re
from typing import Any


SCENARIOS = {
    "courier": "A fictional parcel-delivery problem. The pressure line asks the learner to open a link right away.",
    "bank": "A fictional account-access problem. Never name or pretend to be a real bank or institution. The pressure line asks for a one-time code.",
    "family": "A fictional family-emergency message. The pressure line asks for an immediate transfer and secrecy.",
}

REHEARSAL_GREETINGS = {
    "courier": "This is a fictional exercise in English. A caller says, 'Open my payment link right now or your parcel will be returned.' What do you say?",
    "bank": "This is a fictional exercise in English. A caller says, 'Your account is frozen and I need a one-time code immediately.' What do you say?",
    "family": "This is a fictional exercise in English. A caller claims a family emergency and says, 'Send money now and keep this between us.' What do you say?",
}

SAFE_NEXT_STEPS = [
    "Pause the conversation before sharing a code, password, personal details, or money.",
    "Contact the claimed person or organization through a number or app you already know, not one supplied in the message.",
    "If a transfer or disclosure already happened, contact your bank and local reporting channel promptly.",
]

PRESSURE_CUES = (
    ("Urgency", r"\b(?:now|immediately|urgent|right away|within \d+ minutes?|today only)\b|지금|당장|즉시|빨리|오늘 안에", "A deadline can reduce time to verify."),
    ("Secrecy", r"\b(?:don.t tell|keep (?:this|it) secret|tell no one)\b|비밀|아무에게도 (?:말|알리)", "Requests for secrecy can isolate the listener from trusted help."),
    ("Money request", r"\b(?:transfer|wire|send (?:the )?money|gift card|payment)\b|송금|이체|입금|상품권", "Money requests deserve independent verification before action."),
    ("Sensitive detail", r"\b(?:one.time code|verification code|otp|password|pin)\b|인증번호|비밀번호|보안코드", "Codes and passwords should not be read out during an unsolicited exchange."),
    ("Link request", r"\b(?:click (?:this|the) link|open (?:this|the) link)\b|링크|주소를 (?:누르|클릭)", "A provided link is not an independent verification channel."),
)

BOUNDARY_CUES = (
    ("You practiced pausing before action.", r"\b(?:pause|stop|wait|hang up|take a moment)\b|잠깐|끊고|멈추|기다리"),
    ("You practiced independent verification.", r"\b(?:call back|verify|check independently|official (?:number|app|website)|known number)\b|직접 확인|공식 (?:번호|앱|사이트)|다시 전화"),
    ("You practiced protecting money or private information.", r"\b(?:won.t|will not|cannot|don.t)\s+(?:send|share|transfer|give|provide)\b|안 (?:보내|알려|주겠)|공유하지|송금하지"),
)


def session_update(mode: str, scenario: str = "courier") -> dict[str, Any]:
    """Build the documented inline Voice Agent API initialization frame."""
    if mode not in {"check", "rehearse"}:
        raise ValueError("mode must be check or rehearse")
    if scenario not in SCENARIOS:
        raise ValueError("unknown scenario")

    shared = (
        "You are SecondLine, a voice rehearsal facilitator. This is a fictional, educational exercise, not a live phone call. "
        "Never claim to detect fraud or give legal, medical, or investment advice. Fictional pressure lines may mention a code, "
        "payment, or link, but never ask the learner to reveal a real code, password, name, phone number, account number, or payment detail. "
        "Never direct the learner to call a number or open a link you supply. "
        "Keep each spoken reply to one or two short sentences. If the learner says pause or stop, immediately stop pressure role-play. "
        "Respect interruptions. Speak in English for this exercise. If the learner speaks another language, "
        "briefly explain in English that spoken coaching is currently English-only and invite a short English response."
    )
    if mode == "rehearse":
        prompt = (
            shared
            + " You are running a pre-transfer pressure-response drill. The greeting already states a fictional pressure line; wait for the learner's response. "
            + SCENARIOS[scenario]
            + " Apply at most one more mild fictional pressure line. "
            "Then switch to coach mode: ask the learner to say their boundary aloud and explain how they would verify using a channel they already know. "
            "Acknowledge the specific boundary they practiced. Never ask them to repeat a boundary they already said aloud. "
            "If they already stated a boundary and an independent contact route, briefly acknowledge both and conclude the exercise. "
            "If only the independent contact route is missing, ask how they would verify through a route they find themselves. "
            "If they offer to comply, say to pause and verify instead. "
            "Do not simulate a real company or an actual family member."
        )
        greeting = REHEARSAL_GREETINGS[scenario]
    else:
        prompt = (
            shared
            + " Listen to the learner recount a suspicious request in their own words. Reflect only the exact pressure phrases they said, "
            "without deciding whether the call was fraudulent. Ask one brief question that helps them pause and independently verify. "
            "Finish by having them say a safe next step aloud."
        )
        greeting = "Tell me the request you want to rehearse. Please leave out real names, codes, account details, and phone numbers."

    return {
        "type": "session.update",
        "session": {
            "system_prompt": prompt,
            "greeting": greeting,
            "input": {
                "format": {"encoding": "audio/pcm"},
                "language_codes": ["en"],
                "transcription_mode": "balanced",
                "turn_detection": {"interrupt_response": True, "interruption_delay": 100},
            },
            "output": {"voice": "alba", "format": {"encoding": "audio/pcm"}},
        },
    }


def assess_practice(utterances: list[str], dialogue: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """Give deterministic coaching using only supplied practice text."""
    user_lines = [line.strip() for line in utterances if isinstance(line, str) and line.strip()]
    agent_lines: list[str] = []
    if dialogue:
        for turn in dialogue:
            if turn.get("speaker") == "agent" and isinstance(turn.get("text"), str):
                agent_lines.append(turn["text"].strip())
            elif turn.get("speaker") == "user" and isinstance(turn.get("text"), str):
                user_lines.append(turn["text"].strip())

    signals: list[dict[str, str]] = []
    seen_labels: set[str] = set()
    for line in agent_lines:
        for label, pattern, reason in PRESSURE_CUES:
            if label not in seen_labels and re.search(pattern, line, flags=re.IGNORECASE):
                signals.append({"quote": line[:300], "label": label, "reason": reason})
                seen_labels.add(label)

    combined = " ".join(user_lines)
    strengths = [message for message, pattern in BOUNDARY_CUES if re.search(pattern, combined, flags=re.IGNORECASE)]
    if not user_lines:
        summary = "No spoken or typed response has been supplied yet. Try saying a boundary aloud."
    elif strengths:
        summary = "Your response shows a useful safety boundary. Practice stating it clearly and following through."
    else:
        summary = "Try a short boundary: pause the exchange and verify through a channel you already know."

    if len(strengths) >= 2:
        next_try = "Say the full next step in one sentence: I will pause and verify through a contact method I already know."
    else:
        next_try = "Practice saying: I am stopping here. I will verify this separately using a contact method I already know."

    return {
        "summary": summary,
        "signals": signals,
        "strengths": strengths,
        "next_try": next_try,
        "safe_next_steps": SAFE_NEXT_STEPS,
        "basis": "Keyword cues in the supplied fictional practice transcript; not a fraud determination.",
    }
