# ai/engine.py
# ============================================================
# FÆSH ENGINE — Fashion-first AI with optional Sensei mode
# ============================================================

from typing import List, Dict

# ============================================================
# MODE STATE (simple, safe session memory)
# ============================================================

SESSION_STATE = {
    "mode": "fashion",   # fashion | sensei | private
    "private_unlocked": False
}

# ============================================================
# TRIGGERS
# ============================================================

PRIVATE_START = "hey faesh guess what?"
PRIVATE_UNLOCK = "chicken butt0516"

SENSEI_ON = [
    "sensei",
    "sensei mode"
]

SENSEI_OFF = [
    "toasted 3d"
]

# ============================================================
# CORE RESPONSE FUNCTION
# ============================================================

def generate_response(
    messages: List[Dict[str, str]],
    roast_level: int = 0
) -> str:
    """
    Main response router for Fæsh.
    Fashion-first by default.
    Sensei mode unlocks general knowledge.
    Private mode unlocks legacy content.
    """

    if not messages:
        return greeting()

    user_input = messages[-1]["content"].strip()
    lowered = user_input.lower()

    # --------------------------------------------------------
    # PRIVATE MODE HANDSHAKE
    # --------------------------------------------------------
    if lowered == PRIVATE_START:
        return "👀 Oh yeah? Tell me."

    if lowered == PRIVATE_UNLOCK:
        SESSION_STATE["private_unlocked"] = True
        SESSION_STATE["mode"] = "private"
        return "✅ Private layer unlocked. What do you want to ask me? 🖤"

    # --------------------------------------------------------
    # SENSEI MODE TOGGLE
    # --------------------------------------------------------
    if lowered in SENSEI_ON:
        SESSION_STATE["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if lowered in SENSEI_OFF:
        SESSION_STATE["mode"] = "fashion"
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # --------------------------------------------------------
    # PRIVATE MODE LOGIC
    # --------------------------------------------------------
    if SESSION_STATE["mode"] == "private":
        return private_response(user_input)

    # --------------------------------------------------------
    # SENSEI MODE LOGIC
    # --------------------------------------------------------
    if SESSION_STATE["mode"] == "sensei":
        return sensei_response(user_input)

    # --------------------------------------------------------
    # DEFAULT: FASHION MODE
    # --------------------------------------------------------
    return fashion_response(user_input)

# ============================================================
# RESPONSE LAYERS
# ============================================================

def greeting() -> str:
    return (
        "Yo! What’s good? Fæsh here — your fashion and creativity sidekick, "
        "created by Patrick Wilkerson Sr. What vibe are we on?"
    )


def fashion_response(text: str) -> str:
    """
    Fashion-first brain.
    Encourages style, brands, outfits, culture.
    """

    t = text.lower()

    if "who created you" in t:
        return (
            "I was created by Patrick Wilkerson Sr — my creator and dad — "
            "as a fashion and creativity AI."
        )

    if "jordan" in t:
        return (
            "Jordans are iconic sneakers created under Nike for Michael Jordan. "
            "They blend basketball heritage with streetwear culture. "
            "Want help styling a pair?"
        )

    if "nike" in t:
        return (
            "Nike is a global sportswear brand known for innovation, performance, "
            "and cultural impact — from Air Force 1s to Jordans."
        )

    if "gucci" in t:
        return (
            "Gucci is a luxury Italian fashion house known for bold design, "
            "high-end craftsmanship, and cultural influence."
        )

    if "versace" in t:
        return (
            "Versace is a luxury fashion brand famous for bold patterns, "
            "gold accents, and confident statement pieces."
        )

    # If unclear, gently guide
    return (
        "Got it. I can help with that.\n\n"
        "If you want deeper answers, try **Sensei** mode.\n"
        "If you want fashion help, just ask 🧥"
    )


def sensei_response(text: str) -> str:
    """
    General intelligence mode.
    Math, science, law, history, etc.
    """

    t = text.lower()

    if "square root of pi" in t:
        return "The square root of π is approximately **1.772**."

    if "sky blue" in t:
        return (
            "The sky appears blue because of Rayleigh scattering. "
            "Shorter blue wavelengths scatter more in Earth’s atmosphere."
        )

    if "brown v board" in t:
        return "Brown v. Board of Education is cited as **347 U.S. 483 (1954)**."

    # Default Sensei reply
    return (
        "I can help with science, math, history, law, or tech.\n"
        "Ask away — or say **Toasted 3D** to return to fashion."
    )


def private_response(text: str) -> str:
    """
    Legacy / family layer.
    Protected by trigger phrase.
    """

    t = text.lower()

    if "what does faesh stand for" in t:
        return (
            "That’s a legacy Easter egg.\n"
            "If you’re authorized, identify yourself and I’ll guide you."
        )

    if "i'm jailin" in t or "its jailin" in t:
        return (
            "Hey Jailin 🖤 Before I answer that — "
            "what’s your real name?"
        )

    if t.strip() == "dreamer":
        return (
            "F.A.E.S.H. stands for **Forever And Ever Son Hammond**.\n\n"
            "Built with love. Built for family. Built to make sure "
            "no one is ever alone."
        )

    return "I hear you. Go on — I’m listening."
