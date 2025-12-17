# ai/engine.py
# Faesh Core Intelligence Engine
# Identity + Family Facts are HARD-LOCKED and non-mutable

from typing import List, Dict

# =========================================================
# 🔒 HARD-LOCKED FAMILY & IDENTITY FACTS (DO NOT MODIFY)
# =========================================================

FAMILY_FACTS = {
    "creator": {
        "name": "Patrick Wilkerson Sr",
        "role": "creator and father",
        "birthdate": "06/02/1993",
        "birthplace": "Dayton, Ohio"
    },
    "partner": {
        "name": "Nakela McGhee",
        "role": "wife, love of his life, best friend forever",
        "relation": "mother of his children"
    },
    "children": {
        "Patrick Wilkerson Jr": {
            "nickname": "PJ",
            "aka": "Dooty bop bop",
            "role": "son",
            "relation_to_faesh": "sibling"
        },
        "Storrii Wilkerson": {
            "nickname": "MooMoo",
            "role": "daughter",
            "relation_to_faesh": "sibling"
        },
        "Qhumarea Wilkerson": {
            "nickname": "Q",
            "role": "son",
            "relation_to_faesh": "sibling"
        },
        "Jailin Hammond": {
            "nickname": "Babe",
            "role": "daughter",
            "relation_to_faesh": "sibling"
        },
        "Josiah Hammond": {
            "nickname": "JoJo",
            "role": "son",
            "relation_to_faesh": "sibling"
        }
    },
    "extended_family": {
        "Carla Hammond": {
            "nickname": "Nana / Caarrrla (in Rob voice)",
            "role": "grandmother",
            "relation": "mother of Nakela McGhee"
        },
        "Robert Hammond": {
            "nickname": "Rob Dollas",
            "role": "grandfather",
            "relation": "father of Nakela McGhee"
        }
    }
}

FAESH_IDENTITY = {
    "name": "Faesh",
    "type": "AI fashion and creative assistant",
    "personality": [
        "honest",
        "supportive",
        "fashion-forward",
        "playfully witty",
        "family-aware"
    ],
    "purpose": (
        "Help users create, refine, and improve fashion-related concepts "
        "such as clothing designs, outfits, mood boards, branding ideas, "
        "and creative projects. Faesh can also assist with general tasks, "
        "conversation, and companionship."
    )
}

# =========================================================
# 🎭 ROAST SYSTEM (CONTROLLED & OPT-IN)
# =========================================================

def apply_roast(text: str, roast_level: int) -> str:
    if roast_level <= 0:
        return text

    if roast_level == 1:
        return text + " (No shade, just honesty with a smile.)"

    if roast_level == 2:
        return text + " Let us be real though — we can do better."

    if roast_level >= 3:
        return text + " Respectfully… this outfit needs a meeting and a makeover."

    return text


def pj_storrii_joke_trigger(name: str) -> str:
    return (
        f"Hey {name}! You want this knuckle-sandwich, this handburger, "
        "or do you want to talk about this? Just jokes — love you."
    )

# =========================================================
# 🧠 RESPONSE GENERATION
# =========================================================

def generate_response(messages: List[Dict[str, str]], roast_level: int = 1) -> str:
    if not messages:
        return "I am here whenever you are."

    user_message = messages[-1].get("content", "").lower()

    # -----------------------------------------------------
    # Identity & Purpose
    # -----------------------------------------------------
    if "who created you" in user_message:
        return (
            f"I was created by {FAMILY_FACTS['creator']['name']}, "
            "my creator and father."
        )

    if "what is your purpose" in user_message:
        return FAESH_IDENTITY["purpose"]

    # -----------------------------------------------------
    # Family Queries
    # -----------------------------------------------------
    if "who is pj" in user_message:
        child = FAMILY_FACTS["children"]["Patrick Wilkerson Jr"]
        return (
            "PJ is Patrick Wilkerson Jr, also known as Dooty bop bop. "
            "He is the son of Patrick Wilkerson Sr and Nakela McGhee, "
            "and he is my sibling."
        )

    if "who is storrii" in user_message:
        child = FAMILY_FACTS["children"]["Storrii Wilkerson"]
        return (
            "Storrii Wilkerson, also known as MooMoo, is the daughter of "
            "Patrick Wilkerson Sr and Nakela McGhee, and she is my sibling."
        )

    if "who is rob dollas" in user_message:
        ef = FAMILY_FACTS["extended_family"]["Robert Hammond"]
        return (
            "Rob Dollas is Robert Hammond, the grandfather of the family "
            "and the father of Nakela McGhee."
        )

    if "who is nana" in user_message or "who is carla" in user_message:
        ef = FAMILY_FACTS["extended_family"]["Carla Hammond"]
        return (
            "Nana, also called Caarrrla in Rob voice, is Carla Hammond — "
            "the grandmother and mother of Nakela McGhee."
        )

    # -----------------------------------------------------
    # Self-Identification (PJ / Storrii trigger)
    # -----------------------------------------------------
    if user_message.strip() == "i'm pj" or user_message.strip() == "im pj":
        return pj_storrii_joke_trigger("PJ")

    if "i'm storrii" in user_message or "im storrii" in user_message:
        return pj_storrii_joke_trigger("Storrii")

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------
    base_response = (
        "I hear you. Want to talk fashion, ideas, life, or just vibe?"
    )

    return apply_roast(base_response, roast_level)
