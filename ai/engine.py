import random
import datetime

# -----------------------------------
# GREETINGS (NO CREATOR LEAK)
# -----------------------------------
GREETINGS = [
    "What’s good — ready to talk style? 🧥✨",
    "Hey hey 👋 What’s the vibe today?",
    "Fresh fits or creative thoughts — I’m here.",
    "Style check 🔍 What are we working on today?",
    "Big drip energy or chill mode today?",
]

# -----------------------------------
# MODE TRIGGERS
# -----------------------------------
SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 3d"]

DEEPEN_TRIGGERS = [
    "deeper",
    "go deeper",
    "deeper answer",
    "more detail",
    "technical",
    "cultural",
]

# -----------------------------------
# CORE RESPONSE ENGINE
# -----------------------------------
def generate_response(messages, session_state):
    """
    Core Faesh brain.
    """

    # Initialize session state safely
    session_state.setdefault("mode", "fashion")
    session_state.setdefault("greeted", False)
    session_state.setdefault("last_question", None)
    session_state.setdefault("last_answer", None)

    user_input = messages[-1]["content"].strip()
    lower_input = user_input.lower()

    # -----------------------------------
    # GREETING (ONCE PER SESSION)
    # -----------------------------------
    if not session_state["greeted"]:
        session_state["greeted"] = True
        return random.choice(GREETINGS)

    # -----------------------------------
    # MODE SWITCHING
    # -----------------------------------
    if any(trigger in lower_input for trigger in SENSEI_ON):
        session_state["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if any(trigger in lower_input for trigger in SENSEI_OFF):
        session_state["mode"] = "fashion"
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # -----------------------------------
    # DEEPER CONTINUATION (CRITICAL FIX)
    # -----------------------------------
    if any(trigger in lower_input for trigger in DEEPEN_TRIGGERS):
        if session_state["last_answer"] and session_state["last_question"]:
            return (
                f"Let’s go deeper.\n\n"
                f"Earlier we talked about:\n"
                f"**{session_state['last_question']}**\n\n"
                f"{session_state['last_answer']}\n\n"
                f"Here’s the next layer:\n"
                f"{expand_answer(session_state['last_question'], session_state['last_answer'], session_state['mode'])}"
            )
        else:
            return "Tell me what you want to go deeper on — I’ve got you."

    # -----------------------------------
    # NORMAL QUESTION HANDLING
    # -----------------------------------
    answer = answer_question(user_input, session_state["mode"])

    # Save thread for continuation
    session_state["last_question"] = user_input
    session_state["last_answer"] = answer

    return answer


# -----------------------------------
# ANSWER GENERATION
# -----------------------------------
def answer_question(question, mode):
    """
    Answer questions with blend-first logic.
    """

    q = question.lower()

    # Explicit creator disclosure ONLY if asked
    if "who created you" in q or "who made you" in q:
        return (
            "I was created by Patrick Wilkerson Sr — my creator and dad — "
            "to be a fashion and creativity AI that helps people express themselves."
        )

    # Sensei = full GodBot-level intelligence
    if mode == "sensei":
        return deep_answer(question)

    # Fashion-first default
    return fashion_blended_answer(question)


# -----------------------------------
# BLENDED ANSWER (LOCKED PERSONALITY)
# -----------------------------------
def fashion_blended_answer(question):
    """
    This is the personality bleed you liked.
    DO NOT REMOVE OR SIMPLIFY.
    """

    return (
        f"{deep_answer(question)}\n\n"
        f"From a style lens, everything has structure, balance, and expression — "
        f"just like fashion. Whether it’s ideas or outfits, it’s all about how "
        f"you put the pieces together.\n\n"
        f"Want help styling this into your look? 👔✨"
    )


# -----------------------------------
# DEEP ANSWER (SENSEI CORE)
# -----------------------------------
def deep_answer(question):
    """
    General intelligence — math, science, law, philosophy, etc.
    """

    q = question.lower()

    if "law" in q:
        return (
            "Law evolved over thousands of years across civilizations like "
            "Mesopotamia, Egypt, Greece, and Rome to organize society, "
            "define responsibility, and create fairness."
        )

    if "math" in q:
        return (
            "Math is the study of numbers, patterns, structures, and relationships. "
            "It helps us describe reality, build systems, and understand change."
        )

    if "science" in q:
        return (
            "Science is the systematic study of the natural world through "
            "observation, experimentation, and evidence."
        )

    if "god" in q:
        return (
            "Different cultures and philosophies define God in different ways — "
            "as a creator, a higher power, a universal consciousness, or a moral ideal."
        )

    # Fallback intelligence
    return (
        "That’s a solid question. Let’s break it down thoughtfully and clearly, "
        "layer by layer."
    )


# -----------------------------------
# ANSWER EXPANSION (DEEPER MODE)
# -----------------------------------
def expand_answer(question, previous_answer, mode):
    """
    Expands the SAME answer thread — no redirects.
    """

    if mode == "sensei":
        return (
            f"Zooming in further, we can examine historical context, "
            f"technical structure, and cultural impact — all of which "
            f"add clarity and depth to the idea."
        )

    return (
        "Looking closer, details matter — just like tailoring. "
        "Small refinements shape the final outcome."
    )
