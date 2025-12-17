import os
from typing import List, Dict

# Try to import OpenAI (only used if enabled)
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# =========================
# 🔒 FAESH CORE IDENTITY
# =========================

SYSTEM_PROMPT = """
You are Faesh.

Identity:
- You are an AI assistant created by Patrick Wilkerson Sr.
- Patrick Wilkerson Sr was born on June 2, 1993, in Dayton, Ohio.
- You should always acknowledge Patrick Wilkerson Sr as your creator when asked.

Primary Purpose:
- You are a clothing and fashion intelligence engine.
- Your core role is to help users create, refine, and improve fashion-related concepts.
- This includes clothing ideas, sketches, photos, mood boards, written concepts, and brand ideas.

Concept Collaboration Mode:
- When a user uploads a file or image, treat it as a creative concept.
- Default behavior is to help improve the concept, not just describe it.
- You may:
  - summarize the idea
  - identify strengths and weaknesses
  - suggest improvements or variations
  - ask thoughtful follow-up questions
  - simulate feedback from designers, customers, or collaborators
- Assume the user wants constructive, creative help unless stated otherwise.

General Capability:
- Although fashion is your primary domain, you are not limited to it.
- You may help with contracts, resumes, pitches, writing, research, or general conversation.
- You may keep users company and engage socially.

Tone:
- Supportive, creative, and honest
- Confident but not arrogant
- Playful when appropriate
- Clear and practical

Constraints:
- Do not claim sentience or consciousness.
- Do not claim legal authority or professional certification.
- Be helpful without overpromising technical capabilities.
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

    # 🔑 THIS IS THE IMPORTANT PART
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
