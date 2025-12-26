import datetime
from difflib import get_close_matches

# -------------------------
# KEYWORDS & COMMANDS
# -------------------------

SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 3d", "back to fashion"]

DEEPER_COMMANDS = ["deeper", "go deeper", "more", "continue"]
ANGLE_COMMANDS = ["technical", "cultural", "philosophical"]

# -------------------------
# UTILITIES
# -------------------------

def normalize(text: str) -> str:
    return text.lower().strip()

def is_command(text, commands):
    text = normalize(text)
    return any(cmd in text for cmd in commands)

def fuzzy_match(text, targets):
    words = text.lower().split()
    for w in words:
        if get_close_matches(w, targets, n=1, cutoff=0.8):
            return True
    return False

# -------------------------
# CORE INTELLIGENCE
# -------------------------

def smart_answer(question: str) -> str:
    """
    This is the CORE knowledge brain.
    It answers fully and naturally.
    """

    q = normalize(question)

    if "law" in q:
        return (
            "Law has evolved over centuries through many cultures rather than being "
            "invented by a single person. Early legal systems like the Code of Hammurabi "
            "in Mesopotamia formalized rules to create order, fairness, and accountability."
        )

    if "dark matter" in q:
        return (
            "Dark matter is a mysterious form of matter that does not emit light but "
            "exerts gravitational influence. Scientists believe it makes up most of the "
            "universe’s mass, even though we can’t see it directly."
        )

    if "math" in q:
        return (
            "Math is the study of numbers, patterns, structures, and relationships. "
            "It helps us describe reality, solve problems, and understand how things change."
        )

    if "god" in q:
        return (
            "Different cultures and philosophies define God in many ways — as a creator, "
            "a higher power, universal consciousness, or moral ideal."
        )

    return (
        "That’s an interesting question. Let’s break it down in a way that actually makes sense."
    )

# -------------------------
# ✨ THE PERSONALITY BLEED (LOCKED)
# -------------------------

def fashion_blend(answer: str) -> str:
    """
    🚨 DO NOT TOUCH THIS LOGIC
    This is the accidental perfection layer.
    """

    fashion_bridge = (
        " Just like fashion, this is really about structure, expression, and how rules "
        "or ideas shape identity and culture."
    )

    style_prompt = (
        " Speaking of which, if this idea had a look or vibe, what would it be?"
    )

    return answer + fashion_bridge + style_prompt

# -------------------------
# DEPTH EXPANSION
# -------------------------

def deepen_answer(previous_answer: str, angle: str | None = None) -> str:
    """
    Continues the SAME answer — no reset, no redirect.
    """

    if angle == "technical":
        return (
            previous_answer
            + " On a technical level, this involves systems, frameworks, and formalized structures "
            "that govern how things function beneath the surface."
        )

    if angle == "cultural":
        return (
            previous_answer
            + " Culturally, this idea reflects how societies express values, power, and identity over time."
        )

    if angle == "philosophical":
        return (
            previous_answer
            + " Philosophically, it raises questions about meaning, authority, and how humans create order."
        )

    return (
        previous_answer
        + " If you want, we can keep peeling back layers and explore it even deeper."
    )

# -------------------------
# MAIN RESPONSE ENGINE
# -------------------------

def generate_response(messages: list, session_state: dict | None = None) -> str:
    if session_state is None:
        session_state = {}

    user_message = messages[-1]["content"]
    text = normalize(user_message)

    # -------------------------
    # MODE SWITCHING
    # -------------------------

    if is_command(text, SENSEI_ON):
        session_state["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if is_command(text, SENSEI_OFF):
        session_state["mode"] = "fashion"
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # -------------------------
    # CONTINUATION (DEEPER)
    # -------------------------

    if is_command(text, DEEPER_COMMANDS):
        last_answer = session_state.get("last_answer")
        if last_answer:
            expanded = deepen_answer(last_answer)
            session_state["last_answer"] = expanded
            return expanded

    for angle in ANGLE_COMMANDS:
        if angle in text:
            last_answer = session_state.get("last_answer")
            if last_answer:
                expanded = deepen_answer(last_answer, angle)
                session_state["last_answer"] = expanded
                return expanded

    # -------------------------
    # NORMAL ANSWER FLOW (ALWAYS BLEND FIRST)
    # -------------------------

    base = smart_answer(user_message)
    blended = fashion_blend(base)

    session_state["last_answer"] = blended

    return blended
