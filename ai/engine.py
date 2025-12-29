import random
import datetime
import re

# =========================================================
# PUBLIC IDENTITY RULES
# - DO NOT reveal creator name unless asked.
# - "blend-first": default answers include a fashion twist.
# - Sensei mode deepens, never redirects away from answering.
# - Deeper/technical/cultural continue SAME thread.
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
        "Hey! Fæsh here — what vibe are we on today?",
        "What’s up 👋 Wanna talk outfits, sneakers, or style?",
        "Yo — let’s build a look 🧥",
        "Hey hey! Outfit inspo or just vibing?",
        "What’s good? Tell me what you’re trying to wear or solve.",
    ]

    opts = holiday + general
    return random.choice(opts)


# -------------------------
# SMALL INTENT HELPERS
# -------------------------
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def _contains_any(text: str, phrases) -> bool:
    t = _norm(text)
    return any(p in t for p in phrases)

def _is_sensei_on(text: str) -> bool:
    return _contains_any(text, ["sensei", "sensei mode", "semsei", "sesei", "senseo"])

def _is_sensei_off(text: str) -> bool:
    # You told me "Toasted 3D"
    return _contains_any(text, ["toasted 3d", "toated 3d"])

def _is_deeper(text: str) -> bool:
    return _contains_any(text, ["deeper", "go deeper", "deeper answer", "more depth", "expand"])

def _is_lens(text: str) -> str | None:
    t = _norm(text)
    if "technical" in t:
        return "technical"
    if "cultural" in t:
        return "cultural"
    if "fashion lens" in t or "style lens" in t or t == "fashion":
        return "fashion"
    return None


# -------------------------
# SAFE, SIMPLE "BRAIN"
# (Replace later with OpenAI calls; this is stable & consistent)
# -------------------------
def _basic_answer(q: str) -> str:
    t = _norm(q)

    # Creator disclosure rule
    if _contains_any(t, ["who created you", "who made you", "who built you", "your creator"]):
        return "I was created by Patrick Wilkerson Sr — my dad — as a fashion and creativity AI."

    if "law" in t and _contains_any(t, ["invented", "created", "who made", "who invented"]):
        return (
            "Law wasn’t invented by one person — it evolved over thousands of years.\n"
            "Early written codes (like Mesopotamia’s Code of Hammurabi) helped standardize rules, "
            "settle disputes, and organize society. Over time, systems in Greece, Rome, and beyond "
            "added courts, rights, and procedures that shaped modern law."
        )

    if "math" in t:
        return "Math is the study of numbers, patterns, structures, and logical relationships."

    if "science" in t:
        return "Science studies the natural world using observation, testing, and evidence."

    if "dark matter star" in t:
        return (
            "A ‘dark matter star’ is mostly theoretical — a proposed object where dark matter plays a major role "
            "in the structure or energy balance. We don’t have confirmed observations of one yet."
        )

    if "dark matter" in t:
        return (
            "Dark matter is an unseen form of matter inferred from gravity — it doesn’t emit light, "
            "but it affects how galaxies rotate and how large-scale structure forms."
        )

    if _contains_any(t, ["what is faesh", "who are you", "what are you"]):
        return "Fæsh is a fashion-and-creativity AI sidekick built to help people express themselves through style."

    if "square root of pi" in t or "sqrt(pi)" in t:
        return "√π ≈ 1.7724538509."

    if "why is the sky blue" in t:
        return (
            "The sky looks blue mainly because of Rayleigh scattering: molecules in the atmosphere scatter "
            "shorter (blue) wavelengths of sunlight more than longer (red) wavelengths."
        )

    return "Got it. What are you trying to figure out — and what’s the vibe?"


def _fashion_twist() -> str:
    return (
        "\n\nFrom a style lens, everything has structure, balance, and expression — just like fashion. "
        "Want me to turn this into a fit idea or a vibe? 👔✨"
    )


def _roast_if_requested(roast_level: int, user_text: str) -> str:
    # Safe roasting: only if roast_level > 0 AND user is being playful
    if roast_level <= 0:
        return ""
    t = _norm(user_text)
    if _contains_any(t, ["roast", "cook me", "flame me"]) or roast_level >= 3:
        # keep it playful
        lines = [
            "Alright… you asked for it 😭",
            "Respectfully… that question came in wearing socks with sandals.",
            "I’m not saying you’re lost… I’m saying Google is filing a missing persons report.",
            "You want a knuckle-sandwich, this handburger, or we gonna talk about it? 😄",
        ]
        return "\n\n" + random.choice(lines)
    return ""


# -------------------------
# THREAD CONTINUATION
# -------------------------
def _continue_thread(session_state: dict, lens: str | None) -> str:
    last_q = session_state.get("thread_question") or ""
    last_a = session_state.get("thread_answer") or ""
    if not last_q or not last_a:
        return "Tell me what you want to go deeper on — ask the question again and I’ll dive in."

    # Expand SAME answer, not a new one.
    if lens == "technical":
        return (
            f"Technical depth on: {last_q}\n\n"
            f"{last_a}\n\n"
            "Technical layer: think of ‘law’ like a system spec — definitions, jurisdiction, procedures, "
            "burdens of proof, and enforcement mechanisms. The ‘tech’ is the architecture: rules + institutions "
            "that keep outcomes consistent (in theory) across cases.\n"
            "If you want, I can go deeper on: codes vs case law, courts, due process, or how precedent works."
        )

    if lens == "cultural":
        return (
            f"Cultural depth on: {last_q}\n\n"
            f"{last_a}\n\n"
            "Cultural layer: law reflects what a society values and fears at a given time — order, property, "
            "family, religion, power. Different cultures built different legal priorities (restoration vs punishment, "
            "individual rights vs community obligations). That’s why laws shift over time."
        )

    # Default “Deeper” = mixed depth
    return (
        f"Deeper on: {last_q}\n\n"
        f"{last_a}\n\n"
        "Deeper layer: written codes were only the start. As societies got larger, they needed courts, "
        "procedures, and legitimacy — who decides, what evidence counts, what rights exist, what appeals are allowed. "
        "Modern law is basically a long evolution of *rules + process + enforcement + legitimacy*."
    )


# -------------------------
# MODE DETECTION
# -------------------------
def _handle_mode_switch(user_text: str, session_state: dict) -> str | None:
    if _is_sensei_on(user_text):
        session_state["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if _is_sensei_off(user_text):
        session_state["mode"] = "fashion"
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    return None


# -------------------------
# CORE RESPONSE ENGINE
# -------------------------
def generate_response(messages: list, session_state: dict, roast_level: int = 0):
    """
    Returns (reply, session_state)
    """

    # Initialize defaults
    if "mode" not in session_state:
        session_state["mode"] = "fashion"

    user_input = (messages[-1].get("content") if messages else "") or ""

    # Mode switch?
    switched = _handle_mode_switch(user_input, session_state)
    if switched:
        return switched, session_state

    # Continue same thread?
    lens = _is_lens(user_input)
    if _is_deeper(user_input) or lens is not None:
        reply = _continue_thread(session_state, lens)
        return reply, session_state

    # Generate base answer
    base = _basic_answer(user_input)

    # Store thread so "Deeper / technical / cultural" can expand it
    session_state["thread_question"] = user_input
    session_state["thread_answer"] = base

    # Sensei mode = answer + invite deeper (NO redirect)
    if session_state["mode"] == "sensei":
        reply = (
            f"{base}\n\n"
            "If you want more depth, just say **Deeper**.\n"
            "You can also say **technical** or **cultural**.\n"
            "Say **Toasted 3D** to return to fashion."
        )
        return reply, session_state

    # Fashion mode = blend-first
    reply = base + _fashion_twist() + _roast_if_requested(roast_level, user_input)
    return reply, session_state
