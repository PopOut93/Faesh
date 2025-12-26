# ai/engine.py

from typing import List, Dict

# -------------------------
# MODE CONSTANTS
# -------------------------
MODE_FASHION = "fashion"
MODE_SENSEI = "sensei"

SENSEI_ON = ["sensei", "sensei mode"]
SENSEI_OFF = ["toasted 3d", "back to fashion"]

DEEPER_TRIGGERS = ["deeper", "go deeper"]
TECHNICAL_TRIGGERS = ["technical", "tech"]
CULTURAL_TRIGGERS = ["cultural", "culture"]

# -------------------------
# SAFE RESPONSE HELPERS
# -------------------------
def safe_text(val):
    return val if isinstance(val, str) and val.strip() else None

# -------------------------
# CORE ENGINE
# -------------------------
def generate_response(
    messages: List[Dict[str, str]],
    session_state: Dict = None
) -> str:
    """
    Crash-proof Faesh engine.
    Always returns a STRING.
    """

    try:
        # -------------------------
        # SESSION INIT
        # -------------------------
        if session_state is None:
            session_state = {}

        mode = session_state.get("mode", MODE_FASHION)
        last_answer = session_state.get("last_answer")

        user_message = messages[-1]["content"].lower().strip()

        # -------------------------
        # MODE SWITCHING
        # -------------------------
        if user_message in SENSEI_ON:
            session_state["mode"] = MODE_SENSEI
            return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

        if user_message in SENSEI_OFF:
            session_state["mode"] = MODE_FASHION
            return "🧥 Fashion mode restored. Back to style, drip, and creativity."

        # -------------------------
        # DEPTH CONTINUATION
        # -------------------------
        if (
            user_message in DEEPER_TRIGGERS
            or user_message in TECHNICAL_TRIGGERS
            or user_message in CULTURAL_TRIGGERS
        ):
            if last_answer:
                return expand_answer(
                    last_answer,
                    depth=user_message
                )
            return "Tell me what you want to go deeper on."

        # -------------------------
        # NORMAL ANSWER FLOW
        # -------------------------
        if mode == MODE_SENSEI:
            answer = sensei_answer(user_message)
        else:
            answer = fashion_blended_answer(user_message)

        # -------------------------
        # SAVE THREAD
        # -------------------------
        session_state["last_answer"] = answer

        return answer

    except Exception as e:
        # 🚑 HARD FAILSAFE — NEVER CRASH
        return "I’m here — try asking that again for me 🖤"

# -------------------------
# ANSWER GENERATORS
# -------------------------
def sensei_answer(prompt: str) -> str:
    """
    Full-power general knowledge.
    NO redirection.
    """
    return (
        f"{general_knowledge(prompt)}\n\n"
        "If you want more depth, just say **Deeper**.\n"
        "Say **Toasted 3D** to return to fashion."
    )

def fashion_blended_answer(prompt: str) -> str:
    """
    🔒 BLEND-FIRST RULE (DO NOT REMOVE)
    """
    return (
        f"{general_knowledge(prompt)}\n\n"
        "From a style lens, everything has structure, balance, and expression — "
        "just like fashion. Want help styling this idea into your look? 👔✨"
    )

def expand_answer(previous: str, depth: str) -> str:
    """
    Continue SAME answer thread.
    """
    return (
        f"{previous}\n\n"
        f"Let’s go {depth} — here’s more detail layered on top."
    )

def general_knowledge(prompt: str) -> str:
    """
    Lightweight safe reasoning.
    (Codex / LLM can replace this later.)
    """
    if "law" in prompt:
        return (
            "Law evolved over thousands of years across civilizations like "
            "Mesopotamia, Egypt, Greece, and Rome to organize society."
        )
    if "math" in prompt:
        return (
            "Math is the study of numbers, patterns, and relationships that help "
            "us describe and understand the world."
        )
    if "dark matter" in prompt:
        return (
            "Dark matter is a mysterious form of matter that doesn’t emit light "
            "but affects the universe through gravity."
        )
    if "god" in prompt:
        return (
            "Different cultures define God in different ways — as a creator, "
            "a higher power, or a universal consciousness."
        )

    return "Tell me more — I’m listening."