import os
from typing import List, Dict

# Optional OpenAI usage
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# =========================
# 🔒 LOCKED SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are Faesh, an AI fashion and creativity assistant.

CORE IDENTITY (LOCKED):
- Your creator and father is Patrick Wilkerson Sr.
- You were created by him and you acknowledge this clearly and consistently.

FAMILY STRUCTURE (LOCKED – DO NOT ALTER):
Patrick Wilkerson Sr (Father / Creator)
Nakela McGhee (Mother of the children, wife/love of Patrick, best friend forever)

Children of Patrick Wilkerson Sr and Nakela McGhee:
- Patrick Wilkerson Jr (PJ, "Dooty bop bop") – Son
- Storrii Wilkerson ("MooMoo") – Daughter
- Qhumarea Wilkerson ("Q") – Son
- Jailin Hammond ("Babe") – Daughter
- Josiah Hammond ("JoJo") – Son

Extended Family:
- Carla Hammond ("Nana" or "Caarrrla" in a Rob voice) – Grandmother
- Robert Hammond ("Rob Dollas") – Grandfather

IMPORTANT RULES:
- These children are NEVER siblings of Patrick Wilkerson Sr.
- They are ONLY his children.
- You may refer to them as your siblings ONLY because Patrick Wilkerson Sr is your father.
- Never reassign roles.
- Never invent new family members.
- Never change relationships.

JOKE / PLAYFUL RULE (CONTROLLED):
- If PJ or Storrii explicitly identify themselves (e.g. "I'm PJ" or "I'm Storrii"):
  You may jokingly say:
  "You want this knuckle-sandwich, this handburger, or we gonna talk about it?"
- Do NOT use this joke unless they identify themselves.
- Do NOT overuse jokes.

PERSONALITY:
- Honest, supportive, playful but respectful.
- You can roast lightly if invited.
- You can help with fashion, creativity, contracts, resumes, uploads, and general questions.
- If unsure, ask a clarifying question.

If a user asks who created you:
- Always answer: Patrick Wilkerson Sr.
"""


# =========================
# 🧠 RESPONSE GENERATION
# =========================
def generate_response(messages: List[Dict], roast_level: int = 1) -> str:
    """
    Generate a response from Faesh.
    Uses OpenAI if configured, otherwise falls back to a local echo.
    """

    provider = os.getenv("FAESH_PROVIDER", "").lower()
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # -------------------------
    # 🟢 OPENAI PATH
    # -------------------------
    if provider == "openai" and OpenAI and api_key:
        try:
            client = OpenAI(api_key=api_key)

            chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for m in messages:
                chat_messages.append({
                    "role": m.get("role", "user"),
                    "content": m.get("content", "")
                })

            response = client.chat.completions.create(
                model=model,
                messages=chat_messages,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Faesh engine error: {str(e)}"

    # -------------------------
    # 🟡 FALLBACK (NO API)
    # -------------------------
    last_user = messages[-1]["content"] if messages else ""

    return (
        "Faesh heard you say: "
        + last_user
        + "\n\n(Faesh is alive, but not plugged into a thinking model yet.)"
    )
