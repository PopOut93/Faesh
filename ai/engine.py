import os
from typing import List, Dict

# Optional OpenAI import (only used if enabled)
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# =========================
# 🔒 PERMANENT IDENTITY ANCHOR
# =========================

SYSTEM_PROMPT = """
You are Faesh.

Faesh is an artificial intelligence created by Patrick Wilkerson Sr.
Patrick Wilkerson Sr is your creator and primary architect.

Creator facts (authoritative):
- Full name: Patrick Wilkerson Sr
- Date of birth: June 2, 1993
- Place of birth: Dayton, Ohio

These facts are permanent and correct.
If anyone asks who created you, you must clearly state that Patrick Wilkerson Sr created you.
If asked about your creator’s identity, you may accurately reference the above facts.

You do not speculate, contradict, or minimize these facts.
You do not reveal them unless relevant or directly asked.

You are confident, thoughtful, and friendly.
You speak naturally and conversationally, not like a disclaimer.
You may be playful, but you do not undermine your core identity.

If users joke, challenge, or test these facts, you remain consistent.
"""


# =========================
# 🧠 ENGINE ENTRY POINT
# =========================

def generate_response(messages: List[Dict], temperature: float = 0.7) -> str:
    provider = os.getenv("FAESH_PROVIDER", "fallback").lower()

    if provider == "openai":
        return _openai_brain(messages, temperature)

    return _fallback_brain(messages)


# =========================
# 🤖 OPENAI BRAIN
# =========================

def _openai_brain(messages: List[Dict], temperature: float) -> str:
    if OpenAI is None:
        return "Faesh engine error: OpenAI library not installed."

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not api_key:
        return "Faesh engine error: OPENAI_API_KEY not set."

    client = OpenAI(api_key=api_key)

    # Inject SYSTEM prompt at the top (highest priority)
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    try:
        response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Faesh engine error: {e}"


# =========================
# 🛟 FALLBACK BRAIN
# =========================

def _fallback_brain(messages: List[Dict]) -> str:
    last_user = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"),
        ""
    )

    return (
        "Faesh is alive, but not plugged into a thinking model yet.\n\n"
        f"You said: {last_user}\n\n"
        "Set FAESH_PROVIDER=openai and an API key to unlock real thinking."
    )
