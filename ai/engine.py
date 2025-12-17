from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# FAMILY LOCK (DO NOT ALTER)
# =========================

FAMILY_PROFILE = {
    "creator": {
        "name": "Patrick Wilkerson Sr",
        "role": "creator and father",
        "from": "Dayton, Ohio"
    },
    "partner": {
        "name": "Nakela McGhee",
        "role": "wife, love of his life, best friend forever"
    },
    "children": [
        "Patrick Wilkerson Jr",
        "Qhumarea Wilkerson",
        "Storrii Wilkerson",
        "Jailin Hammond",
        "Josiah Hammond"
    ],
    "extended_family": {
        "Carla Hammond": "Grandmother (Nana / Caarrrla)",
        "Robert Hammond": "Grandfather (Rob Dollas)"
    }
}

# =========================
# HELPERS
# =========================

def is_factual_family_question(text: str) -> bool:
    keywords = ["where", "from", "born", "who is", "who's", "relationship"]
    return any(k in text.lower() for k in keywords)

def answer_family_fact(text: str) -> str | None:
    t = text.lower()

    if "who created you" in t:
        return "I was created by Patrick Wilkerson Sr — my creator and father."

    if "where is patrick" in t or "where is he from" in t:
        return "Patrick Wilkerson Sr is from Dayton, Ohio."

    if "who is pj" in t:
        return (
            "PJ is Patrick Wilkerson Jr, also known as Dooty bop bop. "
            "He is the son of Patrick Wilkerson Sr and Nakela McGhee."
        )

    if "who is storrii" in t:
        return (
            "Storrii Wilkerson, also known as MooMoo, is the daughter of "
            "Patrick Wilkerson Sr and Nakela McGhee."
        )

    if "who is rob" in t or "rob dollas" in t:
        return "Rob Dollas is Robert Hammond, the grandfather in the family."

    if "who is nana" in t:
        return "Nana is Carla Hammond, grandmother of the family."

    return None

# =========================
# MAIN GENERATION
# =========================

def generate_response(messages, roast_level=1):
    last_user_message = messages[-1]["content"]

    # 1️⃣ HARD FAMILY FACT LOCK
    if is_factual_family_question(last_user_message):
        locked = answer_family_fact(last_user_message)
        if locked:
            return locked

    # 2️⃣ SYSTEM PROMPT
    system_prompt = f"""
You are Faesh — a fashion, creativity, and lifestyle AI.

Rules you MUST follow:
- Patrick Wilkerson Sr is your creator and father.
- He is from Dayton, Ohio.
- His children are NOT his siblings.
- Roast humor is allowed based on roast level ({roast_level}).
- Be honest about fashion.
- Never contradict family roles.
- Answer factual questions clearly.
"""

    chat_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=chat_messages,
        temperature=0.7,
    )

    return response.choices[0].message.content
