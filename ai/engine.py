import random
import datetime

# -------------------------
# GREETING LOGIC
# -------------------------

def random_greeting():
    now = datetime.datetime.now()
    month = now.month

    holiday_greetings = []

    if month == 12:
        holiday_greetings.append("🎄 Hey! Fæsh here — holiday fits on your mind?")
    if month == 10:
        holiday_greetings.append("🎃 What’s good? Fæsh here — spooky season drip ready?")
    if month == 2:
        holiday_greetings.append("❤️ Hey there — need help styling something special?")

    general_greetings = [
        "Hey! Fæsh here — what vibe are we on today?",
        "What’s up 👋 Ready to talk style?",
        "Yo — let’s get into some fashion ideas 🧥",
        "Hey hey! Need outfit inspo or just vibing?",
        "What’s good? Let’s build a look."
    ]

    options = holiday_greetings + general_greetings
    return random.choice(options)


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
    - Always blends fashion unless Sensei mode is active
    - Sensei mode only DEEPENS, never redirects
    """

    if "mode" not in session_state:
        session_state["mode"] = "fashion"

    # First interaction = greeting
    if len(messages) == 1:
        return random_greeting()

    user_input = messages[-1]["content"]
    mode_switch = detect_mode(user_input, session_state)

    if mode_switch:
        return mode_switch

    # -------------------------
    # SENSEI MODE
    # -------------------------
    if session_state["mode"] == "sensei":
        return (
            f"{answer_general_question(user_input)}\n\n"
            "If you want more depth, just say **Deeper**.\n"
            "Say **Toasted 3D** to return to fashion."
        )

    # -------------------------
    # FASHION MODE (DEFAULT)
    # -------------------------
    return fashion_blended_answer(user_input)


# -------------------------
# ANSWER HELPERS
# -------------------------

def answer_general_question(text):
    return f"{basic_answer(text)}"


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

    return "Got it. Tell me more — I’m listening."
