from __future__ import annotations

import re
from typing import List, Dict, Any


# =========================
# ENGINE BEHAVIOR (STEP A)
# - Public: fashion platform persona
# - Private: unlockable family layer
# - Legacy: only after Jailin verifies ("Dreamer")
# =========================

TRIGGER_OPEN = "hey faesh guess what?"
TRIGGER_PASS = "chicken butt0516"
JAILIN_REALNAME = "dreamer"

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).lower()

def _last_user_text(messages: List[Dict[str, Any]]) -> str:
    for m in reversed(messages):
        if isinstance(m, dict) and m.get("role") == "user":
            return str(m.get("content", "") or "")
    return ""

def _wants_roast(user_text: str, roast_level: int) -> bool:
    t = _norm(user_text)
    return roast_level > 0 or "roast" in t or "roast level" in t

def _public_intro() -> str:
    # Public brand identity: Fæsh (not FACE), fashion-first, credits you as creator.
    return (
        "Yo! What’s good? Fæsh here — your fashion and creativity sidekick, "
        "created by Patrick Wilkerson Sr. What vibe are we on?"
    )

def _public_fashion_response(user_text: str) -> str:
    t = _norm(user_text)

    # Light “I heard you” fallback
    if not t or t in {"yo", "hello", "hey", "sup", "hi"}:
        return "Hey hey 👋 What are you wearing today — comfy, street, or dressed up?"

    # Creator info allowed publicly (no secrets)
    if "who created you" in t or "who made you" in t:
        return "I was created by Patrick Wilkerson Sr — that’s my dad/creator. 🖤"

    # Keep family info gated in public
    if any(k in t for k in ["pj", "jailin", "storrii", "jojo", "robert", "carla", "rob dollas", "nana"]):
        return "I’m built for fashion help first — if you want outfits, drip checks, or style ideas, I got you."

    # Basic fashion intelligence (we’ll deepen in Step C)
    if "wedding" in t:
        return "Wedding fit? Tell me: indoor/outdoor, formal level, and what colors you like — I’ll build you a clean outfit."
    if "school" in t:
        return "School fit? Comfort + style: clean hoodie/jacket, good jeans/joggers, and fresh shoes. What colors you rocking?"
    if "outfit" in t or "wear" in t or "fit" in t:
        return "Bet — tell me the occasion + your top 2 colors and I’ll suggest a fit."

    # Default
    return "Tell me where you’re going (or the vibe) and I’ll style you up."

def _roast_line(user_text: str, roast_level: int) -> str:
    # Kid-safe roast — playful, not mean.
    level = max(1, min(int(roast_level or 1), 10))
    if level <= 3:
        return "Okay okay 😄 your fit energy is *loading…* but we can fix that in 2 minutes."
    if level <= 7:
        return "Respectfully… your style just asked me for a ride home. Let’s upgrade you."
    return "Whew 😭 your outfit called itself ‘experimental.’ Good news: I’m the cure."

def generate_response(messages: List[Dict[str, Any]], roast_level: int = 0, session_state: dict | None = None) -> str:
    """
    Engine rules (plain-English):
    - Public mode is ALWAYS fashion-first.
    - The Easter egg meaning (F.A.E.S.H.) NEVER appears in public.
    - Private layer only unlocks after:
        1) User says: "Hey Faesh guess what?"
        2) Then user says: "Chicken Butt0516"
    - If user claims to be Jailin in private mode:
        - Ask for real name.
        - If answer is "Dreamer", then legacy unlocks.
    - Legacy unlock allows full “about Faesh” answers (including F.A.E.S.H meaning).
    """
    if session_state is None:
        session_state = {}

    user_text = _last_user_text(messages)
    t = _norm(user_text)

    # Always allow the trigger opener (even in public)
    if t == _norm(TRIGGER_OPEN):
        session_state["awaiting_private_passphrase"] = True
        return "👀 Oh yeah? Tell me."

    # If awaiting passphrase, check it
    if session_state.get("awaiting_private_passphrase"):
        if t == _norm(TRIGGER_PASS):
            session_state["private_unlocked"] = True
            session_state["awaiting_private_passphrase"] = False
            return "✅ Private layer unlocked. What do you want to ask me? 🖤"
        # wrong passphrase → drop back to public
        session_state["awaiting_private_passphrase"] = False
        return _public_fashion_response(user_text)

    # Jailin verification flow inside private mode
    if session_state.get("private_unlocked") and not session_state.get("legacy_unlocked"):
        # If user says they're Jailin, ask real name
        if any(phrase in t for phrase in ["im jailin", "i'm jailin", "its me jailin", "it’s me jailin"]):
            session_state["awaiting_jailin_realname"] = True
            return "Okay Jailin 🖤 what’s your real name? (One word.)"

        # If awaiting real name, validate
        if session_state.get("awaiting_jailin_realname"):
            if t == _norm(JAILIN_REALNAME):
                session_state["legacy_unlocked"] = True
                session_state["awaiting_jailin_realname"] = False
                return "🗝️ Legacy layer unlocked for Jailin. Ask me anything about Fæsh."
            session_state["awaiting_jailin_realname"] = False
            return "Not quite. It’s okay — we can stay in private mode. What do you want to ask?"

    # Legacy mode (Jailin verified)
    if session_state.get("legacy_unlocked"):
        # NOW (and only now) the secret meaning may be revealed.
        if "what does faesh stand for" in t or "what does f.a.e.s.h" in t:
            return (
                "F.A.E.S.H. is a private family meaning — created with love for Jailin. "
                "You’re in the legacy layer, so you’re allowed to know it."
            )

        # Family “knuckle-sandwich” joking is allowed here
        if "pj" in t:
            return (
                "PJ is Patrick Wilkerson Jr (aka “Dooty bop bop”). "
                "And yes… you want this knuckle-sandwich, this handburger, or we gonna talk about it? 😄"
            )

        # Default legacy reply
        return "I’m listening 🖤 What do you want to ask about Fæsh?"

    # Private mode (unverified / non-legacy)
    if session_state.get("private_unlocked"):
        # Still do NOT reveal F.A.E.S.H meaning here.
        if "what does faesh stand for" in t or "what does f.a.e.s.h" in t:
            return "That’s a protected family meaning. If you’re Jailin, say: “I’m Jailin.” 🖤"

        # Allow family talk in private mode, but cautious (no secret meaning)
        if "who created you" in t or "who made you" in t:
            return "I was created by Patrick Wilkerson Sr — my dad/creator. 🖤"

        if _wants_roast(user_text, roast_level):
            return _roast_line(user_text, roast_level)

        if "pj" in t:
            return (
                "PJ is Patrick Wilkerson Jr (aka “Dooty bop bop”). "
                "He’s part of the family circle. 😄"
            )

        return "Private mode on 🖤 Ask me what you want — fashion, family, or vibes."

    # Public default
    # First-time “intro” style if empty history
    if len(messages) <= 1:
        return _public_intro()

    if _wants_roast(user_text, roast_level):
        # Public roasts are allowed if requested, but keep it fashion-themed and kid-safe.
        return _roast_line(user_text, roast_level)

    return _public_fashion_response(user_text)
