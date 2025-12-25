# ai/engine.py
# =========================
# FÆSH ENGINE — PHASE 1
# Fashion Brain + Sensei Brain
# =========================

import re

# -------------------------
# MODE STATE (in-memory)
# -------------------------
SESSION_STATE = {
    "mode": "fashion"  # default
}

# -------------------------
# TRIGGERS
# -------------------------
SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 3d", "back to fashion"]

# -------------------------
# SIMPLE SPELL FIX
# -------------------------
def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", text.lower().strip())

# -------------------------
# FASHION BRAIN
# -------------------------
def fashion_brain(user_input: str) -> str:
    text = normalize(user_input)

    if "jordan" in text:
        return (
            "Jordans are iconic sneakers created under Nike for Michael Jordan. "
            "They blend basketball heritage with streetwear culture. "
            "Want help styling a pair?"
        )

    if "nike" in text:
        return (
            "Nike is a global sportswear brand known for innovation, performance, "
            "and cultural impact — from Air Force 1s to Jordans."
        )

    if "versace" in text:
        return (
            "Versace is a luxury fashion brand known for bold patterns, "
            "gold accents, and confident statement pieces."
        )

    if "gucci" in text:
        return (
            "Gucci is a high-end fashion house known for Italian craftsmanship, "
            "luxury design, and trend-setting style."
        )

    return (
        "Got it. I can help with that.\n\n"
        "If you want deeper answers, try **Sensei** mode.\n"
        "If you want fashion help, just ask 🧥"
    )

# -------------------------
# SENSEI BRAIN
# -------------------------
def sensei_brain(user_input: str) -> str:
    text = normalize(user_input)

    if "math" in text:
        return (
            "Math is the study of numbers, patterns, structures, and relationships. "
            "It helps us understand logic, quantity, space, and change."
        )

    if "science" in text:
        return (
            "Science is the systematic study of the natural world through observation, "
            "experimentation, and evidence."
        )

    if "god" in text:
        return (
            "Different cultures and philosophies define God in different ways — "
            "as a creator, a higher power, a universal consciousness, or a moral ideal."
        )

    if "sky blue" in text:
        return (
            "The sky appears blue due to Rayleigh scattering — "
            "shorter blue wavelengths scatter more in Earth’s atmosphere."
        )

    return (
        "I can help with science, math, history, law, or tech.\n"
        "Ask away — or say **Toasted 3D** to return to fashion."
    )

# -------------------------
# MAIN ENGINE ROUTER
# -------------------------
def generate_response(messages, roast_level=0):
    user_input = messages[-1]["content"]
    text = normalize(user_input)

    # MODE SWITCHING
    if any(trigger in text for trigger in SENSEI_ON):
        SESSION_STATE["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if any(trigger in text for trigger in SENSEI_OFF):
        SESSION_STATE["mode"] = "fashion"
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # ROUTE TO BRAIN
    if SESSION_STATE["mode"] == "sensei":
        return sensei_brain(user_input)

    return fashion_brain(user_input)
