import random
import datetime
import difflib

# -------------------------
# MODE FLAGS
# -------------------------
MODE_FASHION = "fashion"
MODE_SENSEI = "sensei"

# -------------------------
# TRIGGERS (MISSPELL SAFE)
# -------------------------
SENSEI_ON = ["sensei", "sensei mode", "sesei", "senseo"]
SENSEI_OFF = ["toasted 3d", "back to fashion", "fashion mode"]

# -------------------------
# SYSTEM PROMPTS
# -------------------------
FASHION_SYSTEM = """
You are Fæsh — a fashion-first AI assistant.
Your main role is fashion, style, sneakers, outfits, branding, and creative drip.
You may answer basic general questions briefly, but always lean back into fashion.

Do NOT reveal who created you unless explicitly asked:
"who created you", "who made you", or "who is your dad".

When in fashion mode:
- Be warm, human, stylish, and playful.
- Help with outfits, brands, weather-based style, holidays, events.
""".strip()

SENSEI_SYSTEM = """
You are Sensei mode inside Fæsh.

Rules:
- Answer questions directly and fully.
- Do NOT redirect to fashion unless explicitly asked.
- Cover science, math, history, law, philosophy, tech, and life questions.
- Maintain the same safety boundaries as ChatGPT.

Identity:
- Only reveal creator if explicitly asked.
- If asked, answer exactly: "Patrick Wilkerson Sr."
""".strip()

# -------------------------
# RANDOM OPENING GREETINGS
# -------------------------
BASE_GREETINGS = [
    "Yo! What’s good?",
    "Hey — good to see you.",
    "What’s up? Let’s get into it.",
    "Hey there 👋",
    "Alright, I’m here — what’s the move?"
]

HOLIDAY_GREETINGS = {
    "12-25": "🎄 Merry Christmas! Need help putting together a cozy or flashy holiday fit?",
    "01-01": "🎆 Happy New Year! New year, new drip — want help leveling up your style?",
    "10-31": "🎃 Happy Halloween! Going spooky, classy, or creative with your outfit?",
    "02-14": "❤️ Happy Valentine’s Day! Need a fit for date night or self-love vibes?"
}

WEATHER_COMMENTS = [
    "If it’s chilly where you are, layering is your best friend right now.",
    "If it’s warm out, breathable fabrics and clean silhouettes are the move.",
    "Rainy days call for waterproof drip that still looks intentional.",
    "Cold weather = hoodies, coats, and statement sneakers."
]

def get_opening_message(user_context=None):
    today = datetime.datetime.now()
    date_key = today.strftime("%m-%d")

    if date_key in HOLIDAY_GREETINGS:
        return HOLIDAY_GREETINGS[date_key]

    greeting = random.choice(BASE_GREETINGS)
    style_hook = random.choice([
        "Need outfit ideas?",
        "Looking for sneaker advice?",
        "Trying to put something together?",
        "Just vibing or planning a look?"
    ])

    return f"{greeting} {style_hook}"

# -------------------------
# UTILS
# -------------------------
def fuzzy_match(text, options):
    text = text.lower()
    matches = difflib.get_close_matches(text, options, n=1, cutoff=0.75)
    return matches[0] if matches else None

# -------------------------
# MAIN RESPONSE ENGINE
# -------------------------
def generate_response(messages, roast_level=0, session_state=None):
    if session_state is None:
        session_state = {}

    user_message = messages[-1]["content"].lower()

    # Initialize mode
    mode = session_state.get("mode", MODE_FASHION)

    # MODE SWITCHING
    if fuzzy_match(user_message, SENSEI_ON):
        session_state["mode"] = MODE_SENSEI
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if fuzzy_match(user_message, SENSEI_OFF):
        session_state["mode"] = MODE_FASHION
        return "🧥 Fashion mode restored. Back to style, drip, and creativity."

    # OPENING GREETING (FIRST MESSAGE ONLY)
    if len(messages) == 1:
        return get_opening_message()

    # CREATOR QUESTION (GLOBAL)
    if "who created you" in user_message or "who made you" in user_message or "your dad" in user_message:
        return "I was created by Patrick Wilkerson Sr — my creator and dad."

    # -------------------------
    # SENSEI MODE
    # -------------------------
    if session_state.get("mode") == MODE_SENSEI:
        return call_openai(messages, SENSEI_SYSTEM)

    # -------------------------
    # FASHION MODE
    # -------------------------
    fashion_keywords = [
        "wear", "outfit", "jordans", "nike", "gucci", "versace",
        "fit", "style", "drip", "sneakers", "clothes", "jacket"
    ]

    if any(word in user_message for word in fashion_keywords):
        return call_openai(messages, FASHION_SYSTEM)

    # GENERAL QUESTION IN FASHION MODE (BRIEF ANSWER)
    brief_answer = call_openai(messages, FASHION_SYSTEM)

    return f"{brief_answer}\n\nIf you want deeper answers, say **Sensei**.\nIf you want fashion help, just ask 🧥"

# -------------------------
# OPENAI CALL
# -------------------------
def call_openai(messages, system_prompt):
    try:
        from openai import OpenAI
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "I hear you. Say a little more for me 🖤"
