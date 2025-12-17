import os
import json
import urllib.request
from typing import List, Dict, Optional


DEFAULT_SYSTEM = """You are Faesh GodBot.
You are helpful, direct, and friendly.
Ask clarifying questions only when absolutely necessary.
If you don't know, say so and suggest next steps.
"""


def _last_user_text(messages: List[Dict]) -> str:
    for m in reversed(messages):
        if m.get("role") == "user":
            return m.get("content", "")
    return ""


def _fallback_brain(messages: List[Dict], system: Optional[str] = None) -> str:
    # Safe default when no model is configured
    user_text = _last_user_text(messages).strip()
    if not user_text:
        return "Faesh is awake. Say something and I’ll respond."
    return (
        "Faesh isn’t plugged into a thinking model yet.\n\n"
        f"You said: {user_text}\n\n"
        "Next step: set FAESH_PROVIDER and the provider key in Render so I can generate real answers."
    )


def _openai_chat(messages: List[Dict], system: Optional[str], temperature: float) -> str:
    """
    Uses OpenAI Chat Completions API over HTTPS with urllib (no extra deps).
    Env vars:
      - OPENAI_API_KEY (required)
      - OPENAI_MODEL (optional, default: gpt-4.1-mini)
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _fallback_brain(messages, system)

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()  # change any time
    url = "https://api.openai.com/v1/chat/completions"

    sys_text = (system or "").strip() or DEFAULT_SYSTEM

    payload = {
        "model": model,
        "temperature": float(temperature),
        "messages": [{"role": "system", "content": sys_text}] + [
            {"role": m.get("role", "user"), "content": m.get("content", "")}
            for m in messages
            if m.get("content") is not None
        ],
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
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            return (
                data["choices"][0]["message"]["content"]
                .strip()
            )
    except Exception as e:
        # Don’t crash the app in prod — return readable error
        return f"Faesh engine error calling model: {type(e).__name__}: {e}"


def generate_response(
    messages: List[Dict],
    system: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    """
    Single entrypoint used by FastAPI.
    Switch providers with env var:
      FAESH_PROVIDER = "fallback" | "openai"
    """
    provider = os.getenv("FAESH_PROVIDER", "fallback").strip().lower()

    if provider == "openai":
        return _openai_chat(messages, system=system, temperature=temperature)

    # default
    return _fallback_brain(messages, system=system)

