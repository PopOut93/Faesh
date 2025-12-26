import datetime
from difflib import get_close_matches

# -------------------------
# COMMANDS
# -------------------------

SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 3d", "back to fashion"]

DEEPER_COMMANDS = ["deeper", "go deeper", "more", "continue"]
ANGLE_COMMANDS = ["technical", "cultural", "philosophical"]

# -------------------------
# HELPERS
# -------------------------

def normalize(text):
    return str(text).lower().strip()

def is_command(text, commands):
    text = normalize(text)
    return any(cmd in text for cmd in commands)

# -------------------------
# CORE KNOWLEDGE
# -------------------------

def smart_answer(question):
    q = normalize(question)

    if "law" in q:
        return (
            "Law has evolved over centuries through various cultures and societies, "
            "so it isn't attributed to a single inventor. Early systems like the Code "
            "of Hammurabi helped formalize rules for order and fairness."
        )

    if "dark matter" in q:
        return (
            "Dark matter is a mysterious substance that doesn’t emit light but has mass "
            "and gravity. Scientists believe it makes up most of the universe."
        )

    if "math" in q:
        return (
            "Math is the study of numbers, patterns, structures, and relationships. "
            "It helps us understand logic, quantity, and change."
        )

    if "god" in q:
        return (
            "Different cultures and philosophies describe God in different ways — "
            "as a creator, higher power, or universal consciousness."
        )

    return (
        "That’s a solid question. Let’s unpack it in a way that actually makes sense."
    )

# -------------------------
# 🔒 BLEND-FIRST (DO NOT TOUCH)
# -------------------------

def fashion_blend(answer):
    return (
        answer
        + " Just like fashion, this is about structure, expression, and identity."
        + " Speaking of which, if this idea had a look or vibe, what would it be?"
    )

# -------------------------
# DEPTH ENGINE (SAFE)
# -------------------------

def deepen_answer(previous_answer, angle=None):
    if not previous_answer:
        return "Let’s start from the top — what do you want to explore?"

    if angle == "technical":
        return (
            previous_answer
            + " Technically speaking, this involves formal systems, rules, and frameworks "
            "that operate beneath the surface."
        )

    if angle == "cultural":
        return (
            previous_answer
            + " From a cultural perspective, this reflects how societies shape values "
            "and identity over time."
        )

    if angle == "philosophical":
        return (
            previous_answer
            + " Philosophically, it raises questions about meaning, authority, and order."
        )

    return previous_answer + " We can keep peeling back layers if you want."

# -------------------------
# MAIN ENGINE (CRASH-PROOF)
# -------------------------

def generate_response(messages, session_state=None):
    try:
        if session_state is None or not isinstance(session_state, dict):
            session_state = {}

        user_message = messages[-1]["content"]
        text = normalize(user_message)

        # ---- MODE SWITCHING ----
        if is_command(text, SENSEI_ON):
            session_state["mode"] = "sensei"
            return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

        if is_command(text, SENSEI_OFF):
            session_state["mode"] = "fashion"
            return "🧥 Fashion mode restored. Back to style, drip, and creativity."

        # ---- CONTINUATION ----
        if is_command(text, DEEPER_COMMANDS):
            last = session_state.get("last_answer")
            expanded = deepen_answer(last)
            session_state["last_answer"] = expanded
            return expanded

        for angle in ANGLE_COMMANDS:
            if angle in text:
                last = session_state.get("last_answer")
                expanded = deepen_answer(last, angle)
                session_state["last_answer"] = expanded
                return expanded

        # ---- NORMAL FLOW ----
        base = smart_answer(user_message)
        blended = fashion_blend(base)

        session_state["last_answer"] = blended
        return blended

    except Exception as e:
        # 🚨 NEVER FREEZE AGAIN
        return "I’m here — something tripped me up for a second. Try that again 🖤"
