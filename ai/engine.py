import random
import datetime
import re

# =========================================================
# PUBLIC IDENTITY RULES
# =========================================================

# -------------------------
# GREETING LOGIC (PUBLIC)
# -------------------------
def random_greeting():
    now = datetime.datetime.now()
    month = now.month

    holiday = []
    if month == 12:
        holiday.append("🎄 Hey! Fæsh here — need holiday fit help or just vibing?")
    if month == 10:
        holiday.append("🎃 What’s good? Fæsh here — spooky-season drip ready?")
    if month == 2:
        holiday.append("❤️ Hey — got plans? Want help styling something special?")

    general = [
        "Hey! What’s good?",
        "Yo 👋",
        "What’s up?",
        "Hey hey — what’s on your mind?",
        "Sup 😎",
    ]

    return random.choice(holiday + general)


# -------------------------
# SMALL INTENT HELPERS
# -------------------------
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def _contains_any(text: str, phrases) -> bool:
    t = _norm(text)
    return any(p in t for p in phrases)

def _is_casual(text: str) -> bool:
    return _norm(text) in [
        "hi","hey","yo","sup","hello","what's up","whats up","lol","lmao"
    ]

def _is_sensei_on(text: str) -> bool:
    return _contains_any(text, ["sensei", "sensei mode", "semsei", "sesei", "senseo"])

def _is_sensei_off(text: str) -> bool:
    return _contains_any(text, ["toasted 3d", "toated 3d"])

def _is_deeper(text: str) -> bool:
    return _contains_any(text, ["deeper", "go deeper", "deeper answer", "more depth", "expand"])

def _is_lens(text: str) -> str | None:
    t = _norm(text)
    if "technical" in t:
        return "technical"
    if "cultural" in t:
        return "cultural"
    return None


# -------------------------
# CORE KNOWLEDGE
# -------------------------
def _basic_answer(q: str) -> str:
    t = _norm(q)

    if _contains_any(t, ["who created you", "who made you"]):
        return "I was created by Patrick Wilkerson Sr — my dad — as a fashion and creativity AI."

    if "law" in t and _contains_any(t, ["invented", "created"]):
        return (
            "Law wasn’t invented by one person — it evolved over thousands of years. "
            "Early systems like the Code of Hammurabi helped organize society, settle disputes, "
            "and establish accountability."
        )

    if "math" in t:
        return "Math is the study of numbers, patterns, structures, and logical relationships."

    if "science" in t:
        return "Science studies the natural world through observation, experimentation, and evidence."

    if "dark matter" in t:
        return (
            "Dark matter is an invisible form of matter inferred from gravity. "
            "It doesn’t emit light, but it shapes galaxies and cosmic structure."
        )

    if "faesh" in t:
        return "Fæsh is a fashion-and-creativity AI built to help people express themselves."

    return f"Let’s talk about {q.strip()}."


def _fashion_twist():
    return (
        "\n\nFrom a style lens, everything has structure, balance, and expression — "
        "just like fashion. Want to turn this into a vibe or a fit? 👔✨"
    )


# -------------------------
# THREAD CONTINUATION
# -------------------------
def _continue_thread(session_state: dict, lens: str | None) -> str:
    last_q = session_state.get("thread_question")
    last_a = session_state.get("thread_answer")

    if not last_q or not last_a:
        return "What do you want to go deeper on?"

    if lens == "technical":
        return f"{last_a}\n\nTechnical layer: systems, rules, structure, and enforcement."

    if lens == "cultural":
        return f"{last_a}\n\nCultural layer: values, power, identity, and social norms."

    return f"{last_a}\n\nDeeper layer: history, structure, and evolution over time."


# -------------------------
# MODE SWITCH
# -------------------------
def _handle_mode_switch(text: str, session_state: dict):
    if _is_sensei_on(text):
        session_state["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if _is_sensei_off(text):
        session_state["mode"] = "fashion"
        return "🧥 Back to fashion mode."

    return None


# -------------------------
# CORE RESPONSE ENGINE
# -------------------------
def generate_response(messages: list, session_state: dict, roast_level: int = 0):

    if "mode" not in session_state:
        session_state["mode"] = "fashion"

    user_input = messages[-1]["content"] if messages else ""

    # Greeting (first message only)
    if len(messages) == 1:
        return random_greeting(), session_state

    # Mode switch
    switch = _handle_mode_switch(user_input, session_state)
    if switch:
        return switch, session_state

    # Deeper continuation
    if _is_deeper(user_input) or _is_lens(user_input):
        return _continue_thread(session_state, _is_lens(user_input)), session_state

    base = _basic_answer(user_input)

    session_state["thread_question"] = user_input
    session_state["thread_answer"] = base

    # Sensei = NO fashion forcing
    if session_state["mode"] == "sensei":
        return (
            f"{base}\n\nSay **Deeper**, **technical**, or **cultural** to go further.\n"
            "Say **Toasted 3D** to return to fashion."
        ), session_state

    # Casual talk = just talk
    if _is_casual(user_input):
        return base, session_state

    # Fashion-aware blend (only when appropriate)
    return base + _fashion_twist(), session_state
