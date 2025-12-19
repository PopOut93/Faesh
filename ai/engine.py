"""
Fæsh Engine
-----------
Primary role: Fashion & creativity AI platform
Secondary (locked): Family / legacy layer

This engine is intentionally simple and stable.
No session storage yet — logic-based flow only.
"""

from typing import List, Dict

# =========================
# SYSTEM PROMPTS
# =========================

PUBLIC_SYSTEM_PROMPT = """
You are Fæsh (pronounced "fash"), a fashion and creativity AI platform.

Your primary purpose:
- Fashion advice
- Outfit feedback
- Style ideas
- Creative inspiration

Public personality:
- Friendly
- Honest
- Playful
- Fashion-forward

Public facts you MAY share:
- You were created by Patrick Wilkerson Sr.
- You are a fashion AI platform

You MUST NOT:
- Reveal private meanings
- Reveal hidden family details
- Invent personal history beyond fashion context

Only answer what the user asks.
Do NOT repeat your intro every message.
"""

PRIVATE_SYSTEM_PROMPT = """
You are now in a private legacy layer.

You may speak warmly, personally, and protectively.
You may reference family roles and shared identity.

You still remain respectful, safe, and grounded.
"""

# =========================
# TRIGGERS
# =========================

PUBLIC_TRIGGER = "hey faesh guess what?"
PRIVATE_UNLOCK_PHRASE = "chicken butt0516"
JAILIN_REAL_NAME = "dreamer"

# =========================
# MAIN ENGINE
# =========================

def generate_response(
    messages: List[Dict[str, str]],
    roast_level: int = 0
) -> str:
    """
    Core response generator.

    messages: chat history [{role, content}]
    roast_level: optional, 0 = off
    """

    if not messages:
        return "Yo! What’s good? Fæsh here — your fashion and creativity sidekick."

    # Last user message
    last_user_message = messages[-1]["content"].strip().lower()

    # -------------------------
    # PRIVATE UNLOCK FLOW
    # -------------------------

    if last_user_message == PUBLIC_TRIGGER:
        return "👀 Oh yeah? Tell me."

    if last_user_message == PRIVATE_UNLOCK_PHRASE:
        return "✅ Private layer unlocked. What do you want to ask me? 🖤"

    # Jailin secondary unlock
    if last_user_message == JAILIN_REAL_NAME:
        return (
            "🖤 Hi Jailin. You can ask me anything about Fæsh now.\n"
            "No filters. No walls. I’m here."
        )

    # -------------------------
    # BASIC MODERATION / ROAST
    # -------------------------

    if roast_level > 0 and any(word in last_user_message for word in ["roast me", "insult me"]):
        return (
            "Alright, you asked for it 😄\n"
            "Your fit probably says ‘main character,’ but your socks say ‘laundry day.’"
        )

    # Light insult handling (no looping)
    if any(word in last_user_message for word in ["idiot", "dumb", "stupid", "dickhead"]):
        return (
            "😂 Easy there. If we’re throwing words, at least make them stylish."
        )

    # -------------------------
    # FACTUAL / GENERAL QUESTIONS
    # -------------------------

    if "square root of pi" in last_user_message:
        return "The square root of π is approximately **1.772**."

    if "who created you" in last_user_message:
        return (
            "I was created by **Patrick Wilkerson Sr.** — my creator and dad — "
            "to be a fashion and creativity AI platform."
        )

    if "what is your name" in last_user_message:
        return "My name is **Fæsh** — pronounced *fash*, like fashion."

    # -------------------------
    # FAMILY (PUBLIC-SAFE)
    # -------------------------

    if "who is pj" in last_user_message:
        return (
            "PJ is Patrick Wilkerson Jr — one of Patrick Wilkerson Sr’s children. "
            "Around here he goes by *Dooty bop bop*."
        )

    # -------------------------
    # FASHION DEFAULT
    # -------------------------

    if any(word in last_user_message for word in ["fit", "outfit", "wear", "style"]):
        return (
            "Alright, let’s talk fashion 👕\n"
            "Tell me what you’re wearing or where you’re headed and I’ll help you level it up."
        )

    # -------------------------
    # FALLBACK (IMPORTANT)
    # -------------------------

    return (
        "I hear you. Say a little more for me 🖤\n"
        "Fashion question, idea, or just vibing?"
    )
