import os
import json
import urllib.request
from typing import List, Dict, Optional

DEFAULT_SYSTEM = """You are Faesh GodBot.
You are helpful, direct, and friendly.
Ask clarifying questions only when absolutely necessary.
If you don't know something, say so honestly.
"""

def _last_user_text(messages: List[Dict]) -> str:
    for m in reversed(messages):
        if m.get("role") == "user":
            return m.get("content", "")
    return ""

def _fallback_brain(messages: List[Dict], system: Optional[str] = None) -> str:
    user_text = _last_user_text(messages).strip()
    if not user_text:
        return "Faesh is awake. Say something."
    return (
        "Faesh is alive, but not plugged into a thinking model yet.\n\n"
        f"You said: {user_text}\n\n"
        "Set FAESH_PROVIDER=openai and an API key to unlock real thinking."
    )

def _openai_chat(messages: List[Dict], system: Optional[str], temperature: float) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _fallback_brain(messages, system)

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    url = "https://api.openai.com/v1/chat/completions"

    sys_text = (system or "").strip() or DEFAULT_SYSTEM

    payload = {
        "model": model,
        "temperature": float(temperature),
        "messages": (
            [{"role": "system", "content": sys_text}]
            + [
                {"role": m.get("role", "user"), "content": m.get("content", "")}
                for m in messages
                if m.get("content") is not None
            ]
        ),
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Faesh engine error: {type(e).__name__}: {e}"

def generate_response(
    messages: List[Dict],
    system: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    provider = os.getenv("FAESH_PROVIDER", "fallback").lower()

    if provider == "openai":
        return _openai_chat(messages, system, temperature)

    return _fallback_brain(messages, system)
