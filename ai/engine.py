import random
import datetime

# =========================
# MODE FLAGS (SESSION-LOCAL)
# =========================
SESSION_STATE = {
    "mode": "fashion",      # fashion | sensei
    "last_topic": None,     # store last topic for "deeper"
}

# =========================
# TRIGGERS
# =========================
SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 3d", "back to fashion"]

DEPTH_TRIGGERS = [
    "deeper",
    "go deeper",
    "explain more",
    "keep going",
    "continue",
    "elaborate",
]

# =========================
# OPENING GREETINGS (RANDOM)
# =========================
def random_greeting():
    now = datetime.datetime.now()
    month = now.month

    holiday_lines = [
        "Yo! Holiday drip check 🎄 Need help styling something festive?",
        "It’s that season 👀 Let’s make sure your outfit matches the vibes.",
        "Cold weather, hot fits ❄️🔥 What are we styling today?",
    ]

    standard_lines = [
        "Yo! What’s good? Fæsh here — what vibe are we on?",
        "What’s up 👋 Let’s talk style, sneakers, or ideas.",
        "Fæsh checking in 🧥👟 What are you feeling today?",
        "Ready to level up your look or your thoughts?",
    ]

    if month in [11, 12]:
        return random.choice(holiday_lines)
    return random.choice(standard_lines)

# =========================
# CORE RESPONSE ENGINE
# =========================
def generate_response(messages, roast_level=0):
    user_input = messages[-1]["content"].strip().lower()

    # -------------------------
    # MODE SWITCHING
    # -------------------------
    if user_input in SENSEI_ON:
        SESSION_STATE["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if user_input in SENSEI_OFF:
        SESSION_STATE["mode"] = "fashion"
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # -------------------------
    # DEPTH CONTINUATION
    # -------------------------
    if user_input in DEPTH_TRIGGERS and SESSION_STATE["last_topic"]:
        return expand_topic(SESSION_STATE["last_topic"])

    # -------------------------
    # ROUTING BY MODE
    # -------------------------
    if SESSION_STATE["mode"] == "sensei":
        reply, topic = sensei_answer(user_input)
        SESSION_STATE["last_topic"] = topic
        return reply

    # Default: Fashion Mode
    reply, topic = fashion_answer(user_input)
    SESSION_STATE["last_topic"] = topic
    return reply


# =========================
# SENSEI MODE (FULL ANSWERS)
# =========================
def sensei_answer(text):
    # Math
    if "math" in text:
        return (
            "Math is the study of numbers, patterns, structures, and relationships. "
            "It helps us understand logic, quantity, space, and change — from basic counting "
            "to advanced physics and computer science.",
            "math",
        )

    # God
    if "god" in text:
        return (
            "Different cultures and philosophies define God in different ways — as a creator, "
            "a higher power, a universal consciousness, or a moral ideal. Theology, philosophy, "
            "and science all approach the question differently.",
            "god",
        )

    # Law
    if "law" in text:
        return (
            "Law wasn’t invented by a single person. It evolved over thousands of years through "
            "customs, codes, and institutions — from Hammurabi’s Code to Roman law to modern legal systems.",
            "law",
        )

    # Dark Matter
    if "dark matter" in text:
        return (
            "Dark matter is a mysterious form of matter that doesn’t emit light or energy, "
            "but exerts gravitational effects. Scientists infer its existence by observing how "
            "galaxies rotate and bend light.",
            "dark matter",
        )

    # Fallback
    return (
        "I can help with science, math, history, law, or tech.\n"
        "Ask away — or say **Toasted 3D** to return to fashion.",
        None,
    )


# =========================
# FASHION MODE (BLENDED)
# =========================
def fashion_answer(text):
    # Jordans
    if "jordan" in text:
        return (
            "Jordans are iconic sneakers created under Nike for Michael Jordan — rooted in basketball "
            "but dominant in streetwear. If you want to go deeper, say **Deeper** 👀",
            "jordans",
        )

    # Nike
    if "nike" in text:
        return (
            "Nike is a global sportswear brand known for innovation, performance, and culture — "
            "from Air Force 1s to elite athletic gear.",
            "nike",
        )

    # Versace
    if "versace" in text:
        return (
            "Versace is a luxury fashion house known for bold prints, gold accents, and unapologetic confidence. "
            "It’s maximalism done right.",
            "versace",
        )

    # Creator
    if "who created you" in text:
        return (
            "I was created by Patrick Wilkerson Sr — my creator and dad — as a fashion and creativity AI.",
            "creator",
        )

    # Default fashion nudge
    return (
        "Got it. I can help with that.\n\n"
        "If you want deeper answers, say **Sensei**.\n"
        "If you want fashion help, just ask 🧥",
        None,
    )


# =========================
# DEEPER EXPANSION
# =========================
def expand_topic(topic):
    expansions = {
        "jordans": (
            "Going deeper — Jordans started as performance basketball shoes in the 1980s, "
            "but evolved into cultural symbols tied to music, identity, and self-expression. "
            "Different models carry different historical weight."
        ),
        "math": (
            "Going deeper — math underpins science, engineering, economics, and AI. "
            "Abstract math often finds real-world application decades later."
        ),
        "law": (
            "Going deeper — law reflects societal values at a given time. "
            "As societies evolve, laws change to reflect new ethics and realities."
        ),
        "dark matter": (
            "Going deeper — dark matter makes up roughly 27% of the universe, yet we still don’t know "
            "what it’s made of. It remains one of modern physics’ biggest mysteries."
        ),
        "versace": (
            "Going deeper — Versace’s identity is rooted in power dressing, mythology, and rebellion. "
            "It’s fashion meant to be seen and felt."
        ),
    }

    return expansions.get(
        topic,
        "Going deeper — there’s more here if you want to explore it further."
    )
