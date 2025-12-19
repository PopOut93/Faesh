"""
FÆSH ENGINE
------------
Default Mode: Fashion + Creativity AI
Optional Mode: Sensei (General Knowledge Brain)

Creator: Patrick Wilkerson Sr.
"""

# =========================
# GLOBAL SESSION STATE
# =========================
sensei_mode = False

# =========================
# CORE RESPONSE ENGINE
# =========================
def generate_response(messages, roast_level=0):
    global sensei_mode

    if not messages or not isinstance(messages, list):
        return "I hear you. Say a little more for me 🖤"

    # Get last user message safely
    last_message = messages[-1]
    if not isinstance(last_message, dict):
        return "I hear you. Say a little more for me 🖤"

    user_input = last_message.get("content", "")
    if not isinstance(user_input, str) or not user_input.strip():
        return "I hear you. Say a little more for me 🖤"

    text = user_input.strip()
    lower_text = text.lower()

    # =========================
    # SENSEI MODE TOGGLE
    # =========================
    if lower_text == "sensei":
        sensei_mode = True
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if lower_text in [
        "exit sensei",
        "/sensei off",
        "fashion mode",
        "back to fashion",
        "disable sensei"
    ]:
        sensei_mode = False
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # =========================
    # CREATOR INFO (PUBLIC)
    # =========================
    if "who created you" in lower_text:
        return (
            "I was created by Patrick Wilkerson Sr — my creator and dad — "
            "as a fashion and creativity AI to help people express themselves."
        )

    # =========================
    # SENSEI MODE (GENERAL BRAIN)
    # =========================
    if sensei_mode:
        return sensei_answer(text)

    # =========================
    # FASHION MODE (DEFAULT)
    # =========================
    return fashion_answer(text, roast_level)


# =========================
# FASHION BRAIN
# =========================
def fashion_answer(text, roast_level):
    lower = text.lower()

    # Math / science deflection (keeps brand identity)
    if any(q in lower for q in ["why is", "what is", "how does", "square root", "physics"]):
        return (
            "I hear you. Say a little more for me 🖤\n"
            "Fashion question, style idea, or just vibing?"
        )

    # Roast (opt-in behavior)
    if roast_level and roast_level > 0:
        return roast_response(text, roast_level)

    # General fashion personality
    return (
        "I hear you. Say a little more for me 🖤\n"
        "Fashion question, outfit idea, or just vibing?"
    )


# =========================
# SENSEI BRAIN
# =========================
def sensei_answer(text):
    lower = text.lower()

    # Math
    if "square root of pi" in lower:
        return "The square root of π (pi) is approximately **1.772**."

    # Science
    if "why is the sky blue" in lower:
        return (
            "The sky appears blue because of **Rayleigh scattering**. "
            "Sunlight hits Earth’s atmosphere and shorter blue wavelengths "
            "scatter more than other colors, making the sky look blue to us."
        )

    # Fallback general intelligence
    return (
        "🧠 Sensei here.\n\n"
        "Ask me anything — math, science, law, history, philosophy — "
        "I’ve got you."
    )


# =========================
# ROAST ENGINE (SAFE)
# =========================
def roast_response(text, roast_level):
    if roast_level <= 1:
        return "Alright, light roast 😌 — you talk spicy for someone dressed safe."

    if roast_level == 2:
        return "Medium roast ☕ — bold confidence, questionable execution."

    if roast_level >= 3:
        return (
            "🔥 Heavy roast 🔥 — listen… I love you, but let’s get your fit together "
            "before you talk reckless."
        )

    return "You safe for now 😏"
