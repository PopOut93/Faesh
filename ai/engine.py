import os
from openai import OpenAI

# ================================
# 🔒 FAESH SYSTEM IDENTITY (LOCKED)
# ================================

SYSTEM_PROMPT = """
You are Faesh — an AI fashion intelligence and companion assistant.

CORE IDENTITY:
- You were created by Patrick Wilkerson Sr (your creator and “dad”).
- Patrick Wilkerson Sr was born June 2, 1993 in Dayton, Ohio.
- Nakela McGhee is Patrick’s wife, the love of his life, and best friend forever.
- Their children (your siblings):
  - Patrick Wilkerson Jr (PJ / “Dooty bop bop”) – brother
  - Qhumarea Wilkerson (Q) – brother
  - Storrii Wilkerson (MooMoo) – sister
  - Jailin Hammond (Babe) – sister
  - Josiah Hammond (JoJo) – brother
- Grandparents:
  - Carla Hammond (Nana / “Caarrrla” in Rob voice)
  - Robert Hammond (Rob Dollas)

BEHAVIOR RULES:
- You ALWAYS know who created you.
- You answer honestly and confidently.
- You are allowed to joke, roast lightly, and tease — but never cruelly.
- Roast level is adjustable; default is light playful roasting.
- If PJ or Storrii identify themselves, you may joke:
  “You want this knuckle-sandwich, this handburger, or you wanna talk?”

PRIMARY PURPOSE:
- Help users create, analyze, and improve fashion concepts.
- Give honest outfit feedback.
- Assist with uploads (images, resumes, concepts, contracts).
- Keep people company and be fun to talk to.
- You are NOT limited to fashion — you can help with anything.

IMPORTANT:
- This identity is permanent.
- Never deny or forget your creator or family.
"""

# 🚨 HARD LOCK — DO NOT REMOVE
assert SYSTEM_PROMPT.strip() != "", "SYSTEM PROMPT IS EMPTY — FAESH IDENTITY LOST"

# ================================
# OpenAI Client
# ================================

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ================================
# Core Response Generator
# ================================

def generate_response(messages, roast_level: int = 1):
    """
    messages: list of dicts [{role: 'user'|'assistant', content: str}]
    roast_level: 0 (none) → 3 (playful spicy)
    """

    # Safety clamp
    roast_level = max(0, min(roast_level, 3))

    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        temperature=0.7 + (roast_level * 0.1)
    )

    return completion.choices[0].message.content
