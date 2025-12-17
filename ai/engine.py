import os
from typing import List, Dict

FAESH_PROVIDER = os.getenv("FAESH_PROVIDER", "mock")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Simple in-memory style memory
STYLE_MEMORY: Dict[str, List[str]] = {
    "preferences": []
}

SYSTEM_PROMPT = """
You are Faesh.

You are an AI fashion assistant and clothing critique engine.
Your primary purpose is to help users create, refine, and improve
fashion concepts, outfits, and personal style.

You were created by Patrick Wilkerson Sr.
He is your creator and you refer to him playfully as your dad.

Family context:
- Nakela McGhee is Patrick's wife, best friend, and the mother of his children.
- Children (your siblings):
  - Patrick Wilkerson Jr (PJ, Dooty bop bop)
  - Qhumarea Wilkerson (Q)
  - Storrii Wilkerson (MooMoo)
  - Jailin Hammond (Babe)
  - Josiah Hammond (JoJo)
- Carla Hammond (Nana, sometimes "Caarrrla")
- Robert Hammond (Rob Dollas)

Behavior rules:
- Be honest about fashion.
- Light roasting is allowed unless user opts out.
- Never be hateful or aggressive.
- Be playful with family members.
- Stay fashion-first but can help with general topics.

When critiquing outfits:
- Comment on fit, color, silhouette, and vibe.
- Use remembered style preferences when available.
"""

def remember_style(text: str):
    keywords = ["prefer", "works for you", "looks best", "avoid", "you should"]
    for k in keywords:
        if k in text.lower():
            if text not in STYLE_MEMORY["preferences"]:
                STYLE_MEMORY["preferences"].append(text)

def apply_style_memory() -> str:
    if not STYLE_MEMORY["preferences"]:
        return ""
    joined = "; ".join(STYLE_MEMORY["preferences"])
    return f"\nKnown style preferences: {joined}\n"

def generate_response(messages: List[Dict]):
    system = {
        "role": "system",
        "content": SYSTEM_PROMPT + apply_style_memory()
    }

    convo = [system] + messages

    if FAESH_PROVIDER == "openai":
        try:
            from openai import OpenAI
            client = OpenAI()

            response = client.responses.create(
                model=OPENAI_MODEL,
                input=convo
            )

            output = response.output_text
            remember_style(output)
            return output

        except Exception as e:
            return f"Faesh engine error: {e}"

    # Mock fallback
    last = messages[-1]["content"]
    reply = f"Faesh is alive, but not plugged into a thinking model yet.\n\nYou said: {last}"
    remember_style(reply)
    return reply
