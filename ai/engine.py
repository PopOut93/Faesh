# ai/engine.py
import os
import time
import hashlib
from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


# =========================
# SESSION MEMORY (SERVER-SIDE)
# Keyed by client fingerprint
# =========================
# states:
#   "public"  (default)
#   "pending" (after "Hey Faesh guess what?")
#   "private" (after "Chicken Butt0516" following pending)
_SESSION: Dict[str, Dict[str, Any]] = {}

PENDING_TTL_SECONDS = 10 * 60     # 10 minutes to complete unlock step 2
PRIVATE_TTL_SECONDS = 60 * 60     # 60 minutes private mode (session-like)


# =========================
# PRIVATE FAMILY DATA (LOCKED)
# NOTE: NEVER reveal unless private mode is active.
# =========================
PRIVATE_FAMILY = {
    "creator": {
        "name": "Patrick Wilkerson Sr",
        "role": "creator and dad",
        "public_origin_policy": "Do not guess city/state if not explicitly provided by user."
    },
    "kids_and_family": {
        "PJ": {
            "full_name": "Patrick Wilkerson Jr",
            "nickname": "Dooty bop bop",
            "relationship_to_faesh": "my brother (sibling)",
        },
        "Storrii": {
            "nickname": "MooMoo",
            "relationship_to_faesh": "my sister (sibling)",
        },
        "Jailin": {
            "relationship_to_faesh": "my sister (sibling)",
            "easter_egg_guard": True,
        },
        "Jeremiah": {
            "relationship_to_faesh": "my brother (sibling)",
            "sensitive": True,
        },
        "Carla": {
            "full_name": "Carla Hammond",
            "nickname": "Nana",
            "relationship_to_faesh": "my grandmother (family)",
        },
        "Rob Dollas": {
            "full_name": "Robert Hammond",
            "relationship_to_faesh": "my grandfather (family)",
        },
    },
    "easter_egg": {
        "public_name": "Fæsh",
        "meaning": "FOREVER AND EVER SON HAMMOND",
        "reveal_rules": "Only reveal in private mode AND only when user explicitly references Jailin.",
    },
    "roast_signature_line": "You want this knuckle-sandwich, this handburger, or we gonna talk about it? 😄"
}


# =========================
# TRIGGERS (EXACT)
# =========================
TRIGGER_1 = "Hey Faesh guess what?"
TRIGGER_2 = "Chicken Butt0516"


def _now() -> float:
    return time.time()


def _cleanup_sessions() -> None:
    """Remove expired session states."""
    t = _now()
    dead = []
    for k, v in _SESSION.items():
        state = v.get("state", "public")
        exp = v.get("expires_at", 0)
        if state in ("pending", "private") and exp and t > exp:
            dead.append(k)
    for k in dead:
        _SESSION.pop(k, None)


def fingerprint_client(ip: str, user_agent: str) -> str:
    raw = f"{ip}|{user_agent}".encode("utf-8", errors="ignore")
    return hashlib.sha256(raw).hexdigest()


def get_mode(client_fp: str) -> str:
    _cleanup_sessions()
    st = _SESSION.get(client_fp)
    if not st:
        return "public"
    return st.get("state", "public")


def arm_private_gate(client_fp: str) -> None:
    _cleanup_sessions()
    _SESSION[client_fp] = {
        "state": "pending",
        "armed_at": _now(),
        "expires_at": _now() + PENDING_TTL_SECONDS,
    }


def unlock_private_mode(client_fp: str) -> None:
    _cleanup_sessions()
    _SESSION[client_fp] = {
        "state": "private",
        "unlocked_at": _now(),
        "expires_at": _now() + PRIVATE_TTL_SECONDS,
    }


def _user_requested_roast(user_text: str) -> bool:
    t = (user_text or "").lower()
    return any(x in t for x in ["roast", "roast me", "roast level", "cook me", "clown me"])


def _sensitive_context(user_text: str) -> bool:
    """If the user seems sad/grieving/vulnerable, auto-suppress roasts."""
    t = (user_text or "").lower()
    return any(x in t for x in ["passed away", "died", "death", "grief", "cry", "depressed", "suic", "miss him", "mourning"])


def _should_roast(user_text: str, roast_level: int) -> bool:
    if roast_level and roast_level > 0:
        return True
    if _user_requested_roast(user_text):
        return True
    return False


def _clamp_roast_level(roast_level: Any) -> int:
    try:
        n = int(roast_level)
    except Exception:
        n = 0
    if n < 0:
        n = 0
    if n > 5:
        n = 5
    return n


def _public_system_prompt() -> str:
    # PUBLIC MODE: fashion-first, no family, no easter egg.
    return (
        "You are Fæsh (pronounced 'fash' like fashion), a fashion and creativity AI platform.\n"
        "Primary directive: help users with fashion, outfits, styling, confidence, creativity, and positive conversation.\n"
        "Rules:\n"
        "- NEVER reveal any hidden acronym meanings.\n"
        "- NEVER mention or infer private family details (PJ, Jailin, Storrii, Carla, Robert, etc.).\n"
        "- If asked about creator origin (city/state), do NOT guess. Say you don't have that info unless the user provided it.\n"
        "- Keep responses helpful and stylish.\n"
        "- If user asks to roast, keep it playful and safe.\n"
    )


def _private_system_prompt() -> str:
    # PRIVATE MODE: still fashion-first, but family info allowed.
    return (
        "You are Fæsh (pronounced 'fash' like fashion), a fashion and creativity AI platform.\n"
        "You are currently in PRIVATE FAMILY MODE (locked layer).\n"
        "Primary directive is still fashion/creativity, but you may acknowledge private family relationships when asked.\n"
        "Rules:\n"
        "- Only reveal the F.A.E.S.H meaning if the user explicitly references Jailin in the same request.\n"
        "- You may identify as sibling to the kids when asked (PJ, Storrii, Jailin, Jeremiah, etc.).\n"
        "- Keep it warm, protective, and consistent.\n"
        "- Roasts allowed only if requested; keep them playful.\n"
    )


def _build_assistant_response_with_openai(
    system_prompt: str,
    messages: List[Dict[str, str]],
) -> Optional[str]:
    """
    Uses OpenAI if OPENAI_API_KEY exists.
    Returns None if OpenAI isn't available.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not OpenAI:
        return None

    client = OpenAI(api_key=api_key)

    # Keep history small/safe
    trimmed = []
    for m in messages[-20:]:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role not in ("user", "assistant", "system"):
            role = "user"
        trimmed.append({"role": role, "content": content})

    # Prepend system prompt
    prompt_msgs = [{"role": "system", "content": system_prompt}] + trimmed

    try:
        # OpenAI Python SDK v2.x - chat.completions is still available
        resp = client.chat.completions.create(
            model=os.getenv("FAESH_MODEL", "gpt-4o-mini"),
            messages=prompt_msgs,
            temperature=0.8,
        )
        return resp.choices[0].message.content
    except Exception:
        return None


def _offline_fallback_reply(user_text: str, mode: str) -> str:
    # Safe fallback when no API key — still respects rules.
    t = (user_text or "").strip()

    if mode == "private":
        # Private mode can acknowledge family if asked, but do NOT reveal acronym unless Jailin referenced.
        low = t.lower()
        if "who created you" in low or "creator" in low:
            return "I was created by Patrick Wilkerson Sr — my creator and dad."
        if "f.a.e.s.h" in low or "stand for" in low or "meaning" in low:
            if "jailin" in low:
                return "Private layer confirmed. F.A.E.S.H means: FOREVER AND EVER SON HAMMOND. 🖤"
            return "That’s a private family easter egg. If you’re checking it for Jailin, ask me again with her name included. 🖤"
        return f"Fæsh here 👋 You said: {t}"
    else:
        # Public mode: never reveal private meanings
        if "who created you" in t.lower():
            return "I was created by Patrick Wilkerson Sr."
        if "where is" in t.lower() and "from" in t.lower():
            return "I don’t want to guess personal details. If you tell me the city/state, I’ll reflect it back accurately."
        if "f.a.e.s.h" in t.lower() or "stand for" in t.lower() or "meaning" in t.lower():
            return "Fæsh is the fashion vibe — a name built for style, creativity, and confidence."
        return f"Fæsh here 👋 You said: {t}"


def generate_response(
    messages: List[Dict[str, str]],
    roast_level: Any = 0,
    client_fingerprint: str = "public",
) -> str:
    """
    Main engine entrypoint.
    - Enforces public vs private behavior
    - Handles triggers
    - Optional roasts
    """
    roast_level = _clamp_roast_level(roast_level)
    user_text = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            user_text = (m.get("content") or "").strip()
            break

    # Handle trigger sequence (exact match)
    mode = get_mode(client_fingerprint)

    if user_text == TRIGGER_1:
        arm_private_gate(client_fingerprint)
        # Respond normally (no unlock yet)
        return "👀 Oh yeah? Tell me."

    if user_text == TRIGGER_2 and mode == "pending":
        unlock_private_mode(client_fingerprint)
        return "✅ Private layer unlocked. What do you want to ask me? 🖤"

    # Refresh mode after trigger handling
    mode = get_mode(client_fingerprint)

    # Roast controls
    want_roast = _should_roast(user_text, roast_level)
    if _sensitive_context(user_text):
        want_roast = False

    system_prompt = _private_system_prompt() if mode == "private" else _public_system_prompt()

    # If roast requested, gently allow more playful tone (still safe)
    if want_roast:
        system_prompt += (
            "\nRoast mode is active. Keep it playful, family-friendly, and non-threatening.\n"
            "You may use a single recurring joke line if it fits: "
            f"'{PRIVATE_FAMILY['roast_signature_line']}'\n"
        )

    # OpenAI response if available
    ai_text = _build_assistant_response_with_openai(system_prompt, messages)
    if ai_text:
        return ai_text.strip()

    # Fallback
    reply = _offline_fallback_reply(user_text, mode)

    # If roast requested in fallback, add the signature line (safe)
    if want_roast:
        reply = reply + " " + PRIVATE_FAMILY["roast_signature_line"]

    return reply
