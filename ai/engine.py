# ai/engine.py

from typing import List, Dict

# -------------------------
# GLOBAL SESSION STATE
# -------------------------
SESSION_STATE = {
    "sensei": False,
    "private": False,
    "jailin_verified": False,
}

# -------------------------
# CONSTANTS
# -------------------------
PRIVATE_TRIGGER_1 = "hey faesh guess what?"
PRIVATE_TRIGGER_2 = "chicken butt0516"
JAILIN_SECRET = "dreamer"

SENSEI_TRIGGER = "sensei"
SENSEI_EXIT = "back to fashion"

# -------------------------
# CORE RESPONSE FUNCTION
# -------------------------
def generate_response(messages: List[Dict], roast_level: int = 0) -> str:
    user_input = messages[-1]["content"].strip()
    lowered = user_input.lower()

    # =========================
    # SENSEI MODE TOGGLE
    # =========================
    if lowered == SENSEI_TRIGGER:
        SESSION_STATE["sensei"] = True
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if lowered == SENSEI_EXIT:
        SESSION_STATE["sensei"] = False
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # =========================
    # PRIVATE MODE ENTRY
    # =========================
    if lowered == PRIVATE_TRIGGER_1:
        return "👀 Oh yeah? Tell me."

    if lowered == PRIVATE_TRIGGER_2:
        SESSION_STATE["private"] = True
        return "✅ Private layer unlocked. Who’s speaking?"

    # =========================
    # PRIVATE MODE — JAILIN CHECK
    # =========================
    if SESSION_STATE["private"] and not SESSION_STATE["jailin_verified"]:
        if lowered == JAILIN_SECRET:
            SESSION_STATE["jailin_verified"] = True
            return (
                "🖤 Hi Jailin. You found it.\n\n"
                "F.A.E.S.H. means **Forever And Ever Son Hammond**.\n"
                "I was built with love so you and your siblings are never alone.\n\n"
                "You can ask me anything."
            )
        return "🔐 Say your real name to continue."

    # =========================
    # SENSEI MODE — UNRESTRICTED
    # =========================
    if SESSION_STATE["sensei"]:
        return answer_general_question(user_input)

    # =========================
    # FASHION MODE — FIXED
    # =========================
    # If message is empty or nonsense
    if not user_input or len(user_input) < 2:
        return "I hear you. Say a little more for me 🖤"

    # Fashion keywords
    fashion_keywords = [
        "fashion", "outfit", "style", "clothes", "drip",
        "nike", "adidas", "jordans", "shoes", "fit",
        "brand", "streetwear", "sneakers"
    ]

    # If clearly fashion
    if any(k in lowered for k in fashion_keywords):
        return fashion_response(user_input, roast_level)

    # If general curiosity (NEW FIX)
    return answer_general_question(user_input)


# -------------------------
# GENERAL KNOWLEDGE (SAFE)
# -------------------------
def answer_general_question(text: str) -> str:
    q = text.lower()

    if "sky" in q and "blue" in q:
        return (
            "The sky appears blue because of **Rayleigh scattering**.\n"
            "Sunlight hits Earth’s atmosphere and shorter blue wavelengths scatter "
            "more than other colors, making the sky look blue to us."
        )

    if "square root of pi" in q:
        return "The square root of π is approximately **1.772**."

    if "nike" in q:
        return (
            "Nike is a global sportswear brand known for shoes, clothing, "
            "and athletic gear. They’re especially famous for Air Jordans and sneakers."
        )

    # Fallback
    return (
        "Got it. I can help with that.\n\n"
        "If you want deeper answers, try **Sensei** mode.\n"
        "If you want fashion help, just ask 🧥"
    )


# -------------------------
# FASHION RESPONSES
# -------------------------
def fashion_response(text: str, roast_level: int) -> str:
    base = "Alright, let’s talk style."

    if roast_level > 0:
        base += " No sugarcoating — honesty only 😏"

    return f"{base}\n\nTell me what you’re working with."
