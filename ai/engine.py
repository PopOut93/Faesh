import random
import re

# =========================
# MODE TRIGGERS
# =========================
SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 3d"]

DEEPER_TRIGGERS = [
    "deeper",
    "go deeper",
    "explain more",
    "tell me more",
    "keep going",
]

# =========================
# GREETINGS (RANDOMIZED)
# =========================
OPENINGS = [
    "Yo! What’s good? Fæsh here — your fashion and creativity sidekick. What vibe are we on?",
    "Hey hey 👋 Fæsh checking in. Style, questions, or curiosity today?",
    "What’s poppin’? Fæsh in the building — fashion or facts?",
    "Fæsh here 🧥✨ Ready to talk drip, ideas, or both?",
]

# =========================
# CORE RESPONSE ENGINE
# =========================
def generate_response(messages, roast_level=0):
    """
    Core Faesh brain.
    - Fashion-first personality
    - Sensei = expanded knowledge
    - Deeper = continuation, not mode switch
    """

    last_user_msg = messages[-1]["content"].lower().strip()

    # Initialize session state
    sensei_active = False
    continuing = False

    # Inspect history for mode
    for m in messages:
        if m["role"] == "assistant":
            if "🔥 Sensei mode activated" in m["content"]:
                sensei_active = True
            if "🧥 Fashion mode restored" in m["content"]:
                sensei_active = False

    # Mode switching
    if last_user_msg in SENSEI_ON:
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if last_user_msg in SENSEI_OFF:
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # Deeper continuation
    if any(trigger in last_user_msg for trigger in DEEPER_TRIGGERS):
        continuing = True

    # =========================
    # ANSWER GENERATION
    # =========================
    if sensei_active:
        return sensei_answer(last_user_msg, continuing)

    return fashion_answer(last_user_msg, continuing)


# =========================
# FASHION MODE ANSWERS
# =========================
def fashion_answer(question, continuing):
    base_answer = smart_answer(question)

    fashion_twist = random.choice([
        "Just like fashion, it’s all about structure, expression, and how rules bend over time.",
        "Think of it like an outfit — layers matter, and context makes the statement.",
        "Style and ideas evolve the same way trends do — nothing exists in isolation.",
    ])

    if continuing:
        return f"{base_answer}\n\nLet’s zoom in a bit more 👀\n{fashion_twist}"

    return (
        f"{base_answer}\n\n"
        f"{fashion_twist} "
        f"Want to go deeper, or want me to style this idea into something wearable? 🧥✨"
    )


# =========================
# SENSEI MODE ANSWERS
# =========================
def sensei_answer(question, continuing):
    deep_answer = smart_answer(question, deep=True)

    if continuing:
        return (
            f"{deep_answer}\n\n"
            "We can keep drilling down if you want — history, science, philosophy, whatever angle you choose."
        )

    return (
        f"{deep_answer}\n\n"
        "If you want more depth, just say **Deeper**.\n"
        "Say **Toasted 3D** to return to fashion."
    )


# =========================
# KNOWLEDGE CORE
# =========================
def smart_answer(question, deep=False):
    q = question.lower()

    if "law" in q:
        if deep:
            return (
                "Law didn’t come from a single inventor — it evolved over thousands of years. "
                "Early legal systems like the Code of Hammurabi in Mesopotamia formalized rules "
                "to create order, fairness, and accountability in society."
            )
        return (
            "Law has evolved over centuries through various cultures and societies, "
            "so it’s not attributed to a single inventor. Ancient civilizations like "
            "Mesopotamia laid the groundwork with early legal codes."
        )

    if "math" in q:
        return (
            "Math is the study of numbers, patterns, and relationships — a universal language "
            "used to understand logic, space, and change."
        )

    if "science" in q:
        return (
            "Science is the systematic study of the natural world through observation, "
            "experimentation, and evidence."
        )

    if "dark matter" in q:
        return (
            "Dark matter is a mysterious form of matter that doesn’t emit light but exerts "
            "gravitational effects. Scientists believe it makes up most of the universe’s mass."
        )

    if "who created you" in q:
        return (
            "I was created by Patrick Wilkerson Sr — my creator and dad — as a fashion and creativity AI."
        )

    # Fallback
    return (
        "That’s a great question. I can break it down from a fashion lens, "
        "a technical angle, or a cultural one — your move."
    )
