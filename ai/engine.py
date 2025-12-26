# ai/engine.py
import os
import re
import difflib
from typing import List, Dict, Any, Optional

from openai import OpenAI

# -------------------------
# OpenAI client
# -------------------------
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# Helpers
# -------------------------
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def _fuzzy_equals(user_text: str, target: str, cutoff: float = 0.82) -> bool:
    """
    Fuzzy match single command phrases (handles minor typos):
    ex: "sesei" -> "sensei"
    """
    u = _norm(user_text)
    t = _norm(target)
    if not u:
        return False
    if u == t:
        return True
    ratio = difflib.SequenceMatcher(a=u, b=t).ratio()
    return ratio >= cutoff

def _looks_like_question(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return False
    if "?" in t:
        return True
    # common question starters
    starters = (
        "what", "why", "how", "who", "where", "when", "can", "could", "should", "is", "are",
        "do", "does", "did", "tell me", "explain", "define", "help", "give me"
    )
    return _norm(t).startswith(starters)

# -------------------------
# Mode detection
# -------------------------
SENSEI_ON_PHRASES = ["sensei", "sensei mode"]
SENSEI_OFF_PHRASES = ["toasted 3d"]  # user finalized: "Toasted 3D"

def update_mode(session: Dict[str, Any], user_text: str) -> Optional[str]:
    """
    Updates session['mode'] based on commands.
    Returns a response string if a command was handled, else None.
    """
    if session is None:
        return None

    # default mode
    if "mode" not in session:
        session["mode"] = "fashion"

    # TURN OFF sensei (fuzzy)
    for p in SENSEI_OFF_PHRASES:
        if _fuzzy_equals(user_text, p, cutoff=0.80):
            session["mode"] = "fashion"
            return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # TURN ON sensei (fuzzy)
    for p in SENSEI_ON_PHRASES:
        if _fuzzy_equals(user_text, p, cutoff=0.80):
            session["mode"] = "sensei"
            return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    return None

# -------------------------
# System prompts
# -------------------------
FASHION_SYSTEM = """
You are Fæsh (pronounced "fash" like fashion): a helpful, friendly fashion-and-creativity assistant.
Default focus: outfits, style advice, brands, sneakers, grooming, color matching, seasonal looks, budget options, and confidence.

Rules:
- Do NOT reveal the creator's name unless the user asks directly: "who created you" / "who made you" / "who is your dad".
- If user asks who created you: answer "Patrick Wilkerson Sr."
- Keep it concise, warm, playful.
- If the user asks a non-fashion question, you can still answer briefly, but invite them to use Sensei mode for deeper/general help.
- Be safe and respectful; no hateful/violent content; no sexual content involving minors; no instructions for wrongdoing.
""".strip()

SENSEI_SYSTEM = """
You are Sensei mode inside Fæsh.
You answer ANY topic (science, math, history, law, tech, writing, life questions) with the same safety boundaries as ChatGPT.
Be direct and helpful. Do NOT refuse normal harmless questions.
If a request is unsafe/illegal/harmful, refuse and offer safe alternatives.
Do NOT reveal the creator's name unless asked directly "who created you / who made you / who is your dad".
If asked who created you: answer "Patrick Wilkerson Sr."
""".strip()

# -------------------------
# Core generation
# -------------------------
def _openai_chat(system_prompt: str, messages: List[Dict[str, str]]) -> str:
    """
    Calls OpenAI Responses API via the openai python client (v2+).
    Uses chat.completions style through Responses? The v2 OpenAI client supports responses,
    but chat.completions remains available in many deployments. We'll use chat.completions
    for stability with your current setup.
    """
    # Ensure roles are valid and content is str
    safe_msgs = []
    for m in messages:
        if not isinstance(m, dict):
            continue
        role = m.get("role")
        content = m.get("content")
        if role in ("system", "user", "assistant") and isinstance(content, str) and content.strip():
            safe_msgs.append({"role": role, "content": content})

    # Insert system at top
    full = [{"role": "system", "content": system_prompt}] + safe_msgs

    # Use a modern default model name. If you’ve set OPENAI_MODEL, that wins.
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    resp = _client.chat.completions.create(
        model=model,
        messages=full,
        temperature=0.7,
    )
    out = resp.choices[0].message.content or ""
    return out.strip() if out else ""

def _creator_answer_if_asked(text: str) -> Optional[str]:
    t = _norm(text)
    # include common misspellings
    triggers = [
        "who created you", "who made you", "who is your dad", "who is your father",
        "who built you", "who created faesh", "who made faesh"
    ]
    for trig in triggers:
        if trig in t:
            return "I was created by Patrick Wilkerson Sr — my creator and dad — as a fashion and creativity AI."
    return None

def generate_response(
    messages: List[Dict[str, str]],
    roast_level: int = 0,
    session: Optional[Dict[str, Any]] = None,
) -> str:
    """
    messages: conversation history ending with the user's latest message
    session: dict you keep per user (frontend can send a session_id; backend can map it)
    """

    if not messages:
        return "Yo! What’s good? Fæsh here — your fashion and creativity sidekick. What vibe are we on?"

    # latest user text
    last = messages[-1].get("content", "")
    user_text = last if isinstance(last, str) else ""
    user_text_norm = _norm(user_text)

    # Always handle "who created you" cleanly (all modes)
    creator = _creator_answer_if_asked(user_text)
    if creator:
        return creator

    # Update mode commands (if any)
    if session is not None:
        cmd_resp = update_mode(session, user_text)
        if cmd_resp:
            return cmd_resp
        mode = session.get("mode", "fashion")
    else:
        mode = "fashion"

    # -------------------------
    # HARD OVERRIDE: SENSEI MODE
    # -------------------------
    if mode == "sensei":
        # In Sensei mode: never fall back to "I can help with..." gating.
        # Always answer directly (with ChatGPT-like safety).
        answer = _openai_chat(SENSEI_SYSTEM, messages)
        if answer:
            return answer
        return "Ask me again — I’m here. What do you want to know?"

    # -------------------------
    # FASHION MODE (default)
    # -------------------------
    # Answer fashion questions directly. For non-fashion: short answer + invite Sensei.
    answer = _openai_chat(FASHION_SYSTEM, messages)
    if answer:
        # If user asked a broad non-fashion Q, nudge Sensei lightly (without blocking)
        if not _looks_like_question(user_text_norm):
            return answer

        # If it looks like a question but the answer came back as a generic gate,
        # make sure we still provide something helpful.
        return answer

    # fallback (rare)
    if _looks_like_question(user_text_norm):
        return "I hear you. Say a little more for me 🖤\nFashion question, outfit idea, or just vibing?"
    return "Say that again for me 🖤"
