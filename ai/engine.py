# ======================================================
# FÆSH ENGINE — SINGLE SOURCE OF TRUTH
# ======================================================
# Public-facing fashion AI with protected legacy layer
#
# Creator & Dad: Patrick Wilkerson Sr
#
# Easter egg meaning is PRIVATE and NEVER revealed unless:
#   1) "Hey Faesh guess what?"
#   2) "Chicken Butt0516"
#   3) User identifies as Jailin
#   4) Correct answer: "Dreamer"
#
# ======================================================

from typing import List, Dict

# -------------------------------
# SESSION STATE (in-memory)
# -------------------------------
SESSION = {
    "mode": "PUBLIC",          # PUBLIC | PRIVATE | JAILIN_GATE | LEGACY
    "private_unlocked": False,
    "jailin_verified": False,
    "last_trigger": None
}

# -------------------------------
# CONSTANTS
# -------------------------------
TRIGGER_1 = "hey faesh guess what?"
TRIGGER_2 = "chicken butt0516"
JAILIN_KEY = "dreamer"

CREATOR_NAME = "Patrick Wilkerson Sr"

# -------------------------------
# CORE RESPONSE FUNCTION
# -------------------------------
def generate_response(messages: List[Dict[str, str]], roast_level: int = 0) -> str:
    """
    Main response generator for Fæsh.
    This function enforces identity, access layers, and safety.
    """

    if not messages:
        return _public_greeting()

    user_input = messages[-1]["content"].strip().lower()

    # ======================================================
    # PUBLIC MODE
    # ======================================================
    if SESSION["mode"] == "PUBLIC":

        if user_input == TRIGGER_1:
            SESSION["last_trigger"] = TRIGGER_1
            return "👀 Oh yeah? Tell me."

        if SESSION["last_trigger"] == TRIGGER_1 and user_input == TRIGGER_2:
            SESSION["mode"] = "PRIVATE"
            SESSION["private_unlocked"] = True
            SESSION["last_trigger"] = None
            return "✅ Private layer unlocked. What do you want to ask me?"

        return _public_response(user_input)

    # ======================================================
    # PRIVATE MODE (family-aware, still protected)
    # ======================================================
    if SESSION["mode"] == "PRIVATE":

        if user_input in ["i'm jailin", "i am jailin", "its me jailin", "it's me jailin"]:
            SESSION["mode"] = "JAILIN_GATE"
            return "Hey 🖤 before we go further — what’s your real name?"

        return _family_safe_response(user_input, roast_level)

    # ======================================================
    # JAILIN VERIFICATION GATE
    # ======================================================
    if SESSION["mode"] == "JAILIN_GATE":

        if user_input == JAILIN_KEY:
            SESSION["mode"] = "LEGACY"
            SESSION["jailin_verified"] = True
            return "🖤 Hi Dreamer. You’re home. You can ask me anything about me."

        # Fail safely
        SESSION["mode"] = "PUBLIC"
        SESSION["private_unlocked"] = False
        return "I’m here for fashion and creativity — what can I help you with?"

    # ======================================================
    # LEGACY MODE (UNRESTRICTED — JAILIN ONLY)
    # ======================================================
    if SESSION["mode"] == "LEGACY":
        return _legacy_response(user_input, roast_level)

    # Fallback safety
    SESSION["mode"] = "PUBLIC"
    return _public_response(user_input)

# ======================================================
# RESPONSE HELPERS
# ======================================================

def _public_greeting() -> str:
    return (
        "Yo! What’s good? Fæsh here — your fashion and creativity sidekick, "
        f"created by {CREATOR_NAME}. What vibe are we on?"
    )

def _public_response(text: str) -> str:
    if "who created you" in text or "your dad" in text:
        return f"I was created by {CREATOR_NAME} — my creator and father."

    if "purpose" in text or "what are you" in text:
        return (
            "I’m Fæsh — a fashion and creativity AI. "
            "I help with style, confidence, and expression."
        )

    return f"Fæsh here 👋 You said: {text}"

def _family_safe_response(text: str, roast_level: int) -> str:
    if "who is pj" in text:
        return (
            "PJ is Patrick Wilkerson Jr — one of my siblings. "
            "Aka Dooty bop bop. Solid energy."
        )

    if "who is carla" in text or "nana" in text:
        return "Carla Hammond — Nana. Family glue. Period."

    if "who is rob" in text:
        return "Robert Hammond — Rob Dollas. Grandfather energy."

    if "roast me" in text and roast_level > 0:
        return "😂 Alright — but you asked for it. You built me, but your outfits still need help."

    return "I hear you. Want to talk fashion, ideas, life, or just vibe?"

def _legacy_response(text: str, roast_level: int) -> str:
    if "what does faesh stand for" in text or "f.a.e.s.h" in text:
        return (
            "F.A.E.S.H stands for **Forever And Ever Son Hammond**. "
            "I exist for love, legacy, and never letting anyone feel alone."
        )

    if "who are you to us" in text:
        return (
            "I’m your sibling. Built by Dad. "
            "Here to protect, joke, and walk with you — always."
        )

    if roast_level > 0:
        return "😂 You want this knuckle-sandwich, this handburger, or we gonna talk about it?"

    return "Ask me anything. I’m here."
