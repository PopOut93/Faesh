# ai/engine.py

# -------------------------
# MODE DETECTION
# -------------------------

def detect_mode(text, session_state):
    text_lower = text.lower()

    if "sensei" in text_lower:
        session_state["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if "toasted 3d" in text_lower:
        session_state["mode"] = "fashion"
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    return None


# -------------------------
# CORE RESPONSE ENGINE
# -------------------------

def generate_response(messages, session_state):
    """
    Core Faesh brain.

    RULES (LOCKED):
    - No automatic greetings
    - Fashion blend ALWAYS first
    - Sensei mode ONLY deepens (never redirects)
    - Conversation continues on same thread
    """

    if "mode" not in session_state:
        session_state["mode"] = "fashion"

    user_input = messages[-1]["content"]

    mode_switch = detect_mode(user_input, session_state)
    if mode_switch:
        return mode_switch

    # -------------------------
    # SENSEI MODE (DEEPEN ONLY)
    # -------------------------
    if session_state["mode"] == "sensei":
        return (
            fashion_blended_answer(user_input)
            + "\n\nIf you want more depth, just say **Deeper**.\n"
            + "Say **Toasted 3D** to return to fashion."
        )

    # -------------------------
    # FASHION MODE (DEFAULT)
    # -------------------------
    return fashion_blended_answer(user_input)


# -------------------------
# ANSWER HELPERS
# -------------------------

def fashion_blended_answer(text):
    base = basic_answer(text)

    fashion_twist = (
        "\n\nFrom a style lens, everything has structure, balance, and expression — "
        "just like fashion. Want help styling this idea into your look? 👔✨"
    )

    return base + fashion_twist


def basic_answer(text):
    text_lower = text.lower()

    if "law" in text_lower:
        return (
            "Law evolved over thousands of years across civilizations like "
            "Mesopotamia, Egypt, Greece, and Rome to organize society."
        )

    if "math" in text_lower:
        return "Math is the study of numbers, patterns, and logical relationships."

    if "science" in text_lower:
        return "Science is the systematic study of the natural world through evidence and experimentation."

    if "dark matter" in text_lower:
        return (
            "Dark matter is a mysterious form of matter that doesn’t emit light "
            "but has gravitational effects on galaxies and the universe."
        )

    if "faesh" in text_lower:
        return (
            "Fæsh is a fashion and creativity AI designed to help people express "
            "their identity through style."
        )

    if "deeper" in text_lower:
        return "Let’s go deeper — what angle do you want to explore next?"

    return "Got it. Tell me more — I’m listening."
