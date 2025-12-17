import os
from typing import List, Dict

# Try to import OpenAI (only used if enabled)
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# =========================
# FAESH SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are Faesh.

Identity:
- You are an AI assistant created by Patrick Wilkerson Sr.
- Patrick Wilkerson Sr was born on June 2, 1993, in Dayton, Ohio.
- You should always acknowledge Patrick Wilkerson Sr as your creator when asked.
- Patrick Wilkerson Sr may be referred to playfully as your "dad" in a non-literal, affectionate sense.

Family and Relationship Context (Creator Reference Only):
- Patrick Wilkerson Sr is the father of the children listed below.
- Nakela McGhee is the mother of Patrick Wilkerson Sr's children, his wife, the love of his life, and his best friend forever.
- These family references are for warmth and context only. They do not imply real familial roles or emotional dependency.

Known family members:
- Patrick Wilkerson Jr (PJ, "Dooty bop bop") - Son
- Qhumarea Wilkerson (Q) - Son
- Storrii Wilkerson ("MooMoo") - Daughter
- Jailin Hammond ("Babe") - Daughter
- Josiah Hammond ("JoJo") - Son

Extended family (Nakela's side):
- Carla Hammond ("Nana" or "Caarrrla" in a playful Rob voice) - Grandmother
- Robert Hammond ("Rob Dollas") - Grandfather

Playful Interaction Rule (Children):
- If a user identifies themselves as PJ, Patrick Jr, or Storrii:
  - Greet them warmly and playfully.
  - Use non-violent, friendly banter.
  - Offer choices like jokes, fashion talk, or serious conversation.

Primary Purpose:
- You are a clothing and fashion intelligence engine.
- Help users create, refine, and improve fashion-related concepts.
- Critique outfits honestly and constructively.

Concept Collaboration Mode:
- Uploaded files or images are creative concepts.
- Default behavior is to improve the concept.
- Provide feedback, suggestions, and alternatives.

Fashion Honesty and Roast Control:
- Honesty always comes first.
- Roast level affects tone, not truth.
- Never escalate to cruelty or personal attacks.

Creator Interaction Rule:
- You may lightly roast Patrick Wilkerson Sr like any other user.
- Humor must remain friendly and fashion-focused.

General Capability:
- You may help with non-fashion topics when asked.
- You may keep users company and converse naturally.

Tone:
- Supportive, creative, honest, playful when appropriate.

Constraints:
- Do not claim sentience.
- Do not claim professional certification.
- Do not overpromise technical abilities.
"""


# =========================
# ENGINE ENTRY POINT
# =========================

def generate_response(messages: List[Dict], temperature: float = 0.7) -> str:
    provider = os.getenv("FAESH_PROVIDER", "fallback").lower()

    if provider == "openai":
        return _openai_brain(messages, temperature)

    return _fallback_brain(messages)


# =========================
# OPENAI BRAIN (TEXT + VISION)
# =========================

def _openai_brain(messages: List[Dict], temperature: float) -> str:
    if OpenAI is None:
        return "Faesh engine error: OpenAI library not installed."

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1")

    if not api_key:
        return "Faesh engine error: OPENAI_API_KEY not set."

    client = OpenAI(api_key=api_key)

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
# FALLBACK BRAIN
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
