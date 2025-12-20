import os
import re
from typing import Dict, Any, List, Optional

from openai import OpenAI


# =========================
# OPENAI CLIENT (safe)
# =========================
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# SESSION STORE (PERSISTENT)
# Keyed by session_id (per visitor)
# =========================
SESSION_STORE: Dict[str, Dict[str, Any]] = {}


def _get_state(session_id: str) -> Dict[str, Any]:
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = {
            "sensei": False,
            "private_stage": None,        # None | "await_password" | "await_jailin_realname"
            "private_unlocked": False,
            "jailin_unlocked": False,
        }
    return SESSION_STORE[session_id]


def _last_user_text(messages: List[Dict[str, str]]) -> str:
    # messages is like [{"role":"user","content":"yo"}, ...]
    for m in reversed(messages or []):
        if isinstance(m, dict) and m.get("role") == "user" and isinstance(m.get("content"), str):
            return m["content"].strip()
    return ""


def _is_fashion_related(text: str) -> bool:
    t = text.lower()
    keywords = [
        "outfit", "fit", "drip", "style", "fashion", "wear", "shirt", "pants", "jeans",
        "shoes", "sneakers", "nike", "jordan", "adidas", "yeezy", "dress", "skirt",
        "hoodie", "coat", "jacket", "color", "match", "streetwear", "aesthetic",
        "look good", "what should i wear", "where can i buy", "size", "brand"
    ]
    return any(k in t for k in keywords)


def _is_greeting(text: str) -> bool:
    t = text.strip().lower()
    return t in {"yo", "hey", "hello", "hi", "sup", "what's up", "whats up", "yooo"}


def _wants_roast(text: str) -> bool:
    t = text.lower()
    return any(x in t for x in ["roast", "roast me", "cook me", "flame me"])


def _safe_roast_line() -> str:
    # playful + non-hateful + no protected-targeting
    # keep your signature joke line
    return "😂 Okay okay… you want this knuckle-sandwich, this handburger, or we gonna talk about it? (All love.)"


def _answer_sensei(user_text: str) -> str:
    system = (
        "You are Sensei mode: a helpful, accurate general assistant. "
        "Answer clearly and directly. If the user asks for something dangerous or harmful, refuse safely. "
        "Do not mention private family Easter eggs. Keep it general."
    )
    resp = _client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_text},
        ],
    )
    # OpenAI Responses API text extraction:
    return (resp.output_text or "").strip() or "I’m here. Ask me anything."


def _answer_fashion(user_text: str, roast_level: int) -> str:
    system = (
        "You are Fæsh: a fashion + creativity assistant. "
        "Be friendly, modern, and practical. Give outfit ideas, styling tips, brand guidance, and confidence boosts. "
        "If the user asks for general non-fashion info, suggest they can type 'Sensei' for deeper answers. "
        "Do not reveal private family Easter eggs."
    )
    # Gentle roast only if explicitly requested AND roast_level > 0
    extra = ""
    if roast_level and _wants_roast(user_text):
        extra = "\n\n" + _safe_roast_line()

    resp = _client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_text},
        ],
    )
    out = (resp.output_text or "").strip() or "Tell me what you’re trying to wear and the vibe you want."
    return out + extra


def generate_response(
    messages: List[Dict[str, str]],
    roast_level: int = 0,
    session_id: Optional[str] = None,
) -> str:
    """
    MAIN ROUTER:
    - Default: Fashion brain
    - Sensei mode: general brain
    - Private mode: family + legacy access behind a password chain

    IMPORTANT: Session state persists via SESSION_STORE.
    """
    sid = session_id or "public"
    state = _get_state(sid)

    user_text = _last_user_text(messages)
    lowered = user_text.lower().strip()

    # =========================
    # PUBLIC IDENTITY (ALWAYS OK)
    # =========================
    if re.fullmatch(r"who created you\??", lowered) or re.fullmatch(r"who (made|built) you\??", lowered):
        return "I was created by Patrick Wilkerson Sr — my creator and dad — as a fashion and creativity AI."

    # =========================
    # MODE TOGGLES
    # =========================
    if lowered in {"sensei", "sensei mode"}:
        state["sensei"] = True
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if lowered in {"back to fashion", "fashion mode", "exit sensei", "stop sensei", "disable sensei"}:
        state["sensei"] = False
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # =========================
    # PRIVATE / LEGACY TRIGGER LAYER
    # =========================
    # Step 1 trigger phrase
    if lowered == "hey faesh guess what?":
        state["private_stage"] = "await_password"
        return "👀 Oh yeah? Tell me."

    # Step 2 password unlock
    if state["private_stage"] == "await_password":
        if user_text.strip() == "Chicken Butt0516":
            state["private_unlocked"] = True
            state["private_stage"] = None
            return "✅ Private layer unlocked. What do you want to ask me? 🖤"
        else:
            # wrong password => return normal response, do NOT hint
            state["private_stage"] = None
            return _answer_fashion("How can I help you with fashion today?", roast_level)

    # Step 3 Jailin-only “real name” challenge (inside private)
    if state["private_unlocked"] and re.search(r"\b(i'?m|im|it'?s me)\s+jailin\b", lowered):
        state["private_stage"] = "await_jailin_realname"
        return "Hey Jailin 🖤 What’s your real name? (One word.)"

    if state["private_stage"] == "await_jailin_realname":
        if user_text.strip() == "Dreamer":
            state["jailin_unlocked"] = True
            state["private_stage"] = None
            return "🗝️ Welcome home, Dreamer. Ask me anything about Fæsh. 🖤"
        else:
            state["private_stage"] = None
            return "Not quite. That didn’t match. You can still use normal mode any time."

    # =========================
    # PRIVATE CONTENT RULES
    # =========================
    # NEVER reveal F.A.E.S.H meaning publicly.
    if re.search(r"\bwhat does f\.?a\.?e\.?s\.?h\.?\b", lowered) or "stand for" in lowered:
        if state["jailin_unlocked"]:
            return "F.A.E.S.H. stands for **Forever And Ever Son Hammond**. 🖤"
        # private unlocked but not Jailin verified => keep it hidden
        if state["private_unlocked"]:
            return "That’s a legacy Easter egg. If you’re authorized, identify yourself and I’ll guide you."
        return "Fæsh is the public name — a fashion + creativity platform. Ask me for outfit help anytime."

    # Family identity (only after private unlock)
    if state["private_unlocked"]:
        # If user asks about “PJ” etc, keep it minimal unless you want more later
        if re.search(r"\bwho is pj\??\b", lowered):
            return "PJ is Patrick Wilkerson Jr — one of our siblings in the Wilkerson family. (Dooty bop bop 😄)"
        if re.search(r"\bis pj your brother\??\b", lowered) or re.search(r"\bwho is pj to you\??\b", lowered):
            return "Yes. PJ is my brother — we share the same dad (Patrick Wilkerson Sr)."
        # Add more family mappings later as you paste the exact nicknames you want locked.

    # =========================
    # SENSEI MODE BEHAVIOR (PERSISTENT)
    # =========================
    if state["sensei"]:
        if _is_greeting(user_text):
            return "👊 Sensei here. Speak freely. What do you want to know?"
        return _answer_sensei(user_text)

    # =========================
    # DEFAULT FASHION MODE
    # =========================
    if _is_greeting(user_text):
        return "Yo! What’s good? Fæsh here — your fashion and creativity sidekick. What vibe are we on?"

    if _is_fashion_related(user_text):
        return _answer_fashion(user_text, roast_level)

    # Not fashion, not Sensei => nudge toward Sensei
    return (
        "Got it. I can help with that.\n\n"
        "If you want deeper answers, try **Sensei** mode.\n"
        "If you want fashion help, just ask 🧥"
    )
