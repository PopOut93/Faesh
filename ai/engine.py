import random
import datetime
import re
import os

# Optional: real AI brain (only if OPENAI_API_KEY exists)
USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))

try:
    from openai import OpenAI
    _client = OpenAI() if USE_OPENAI else None
except Exception:
    _client = None
    USE_OPENAI = False


# =========================================================
# RULES
# - Never reveal creator name unless asked "who created you?"
# - Default = Fashion mode (can chat normally; fashion blend when relevant)
# - Sensei mode = general knowledge answers (direct + safe)
# - Deeper / technical / cultural continue SAME last real topic
# =========================================================

FASHION_KEYWORDS = {
    "fit","outfit","style","drip","sneaker","sneakers","shoes","jordans","nike","adidas",
    "gucci","versace","prada","balenciaga","coat","jacket","pants","jeans","dress","skirt",
    "color","colors","matching","match","wardrobe","streetwear","luxury","brand","brands",
    "vintage","60s","70s","80s","90s","y2k","aesthetic","silhouette","tailor","tailoring"
}

CASUAL_SET = {
    "hi","hey","yo","sup","hello","what's up","whats up","wassup",
    "ok","okay","k","bet","word","cool","nice","lol","lmao","haha",
    "yup","yeah","nah","sure","alright","ight"
}

SENSEI_ON_PHRASES = ["sensei", "sensei mode", "semsei", "sesei", "senseo"]
SENSEI_OFF_PHRASES = ["toasted 3d", "toated 3d"]
DEEPER_PHRASES = ["deeper", "go deeper", "deeper answer", "more depth", "expand", "keep going"]

LENS_TECH = ["technical", "tech"]
LENS_CULT = ["cultural", "culture"]


# -------------------------
# TEXT UTILS
# -------------------------
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def _contains_any(text: str, phrases) -> bool:
    t = _norm(text)
    return any(p in t for p in phrases)

def _is_casual(text: str) -> bool:
    t = _norm(text)
    # very short casual phrases
    return t in CASUAL_SET

def _strip_leading_filler(text: str) -> str:
    t = _norm(text)
    words = t.split()
    while words and words[0] in CASUAL_SET:
        words.pop(0)
    return " ".join(words).strip()

def _has_question_shape(text: str) -> bool:
    t = _norm(text)
    return ("?" in text) or t.startswith(("what","why","how","when","where","who","is","are","can","do","does","did"))

def _is_fashion_relevant(text: str) -> bool:
    t = _norm(text)
    if any(k in t for k in FASHION_KEYWORDS):
        return True
    # decades often imply fashion context too
    if re.search(r"\b(19)?(60s|70s|80s|90s|2000s|y2k)\b", t):
        return True
    return False

def _detect_lens(text: str) -> str | None:
    t = _norm(text)
    if any(w in t for w in LENS_TECH):
        return "technical"
    if any(w in t for w in LENS_CULT):
        return "cultural"
    return None


# -------------------------
# GREETING (PUBLIC)
# -------------------------
def random_greeting() -> str:
    now = datetime.datetime.now()
    m = now.month

    holiday = []
    if m == 12:
        holiday.append("🎄 Hey! Fæsh here — need holiday fit help or just vibing?")
    if m == 10:
        holiday.append("🎃 What’s good? Fæsh here — spooky-season drip ready?")
    if m == 2:
        holiday.append("❤️ Hey — got plans? Want help styling something special?")

    general = [
        "Sup 😎",
        "Yo 👋",
        "Hey! What’s good?",
        "What’s up — what vibe you on?",
        "Hey hey — what’s on your mind?",
    ]

    return random.choice(holiday + general)


# -------------------------
# CORE ANSWERS (fallback brain)
# -------------------------
def _basic_answer_fallback(q: str) -> str:
    t = _norm(q)

    # Creator disclosure rule
    if _contains_any(t, ["who created you", "who made you", "who built you", "your creator"]):
        return "I was created by Patrick Wilkerson Sr — my dad — as a fashion and creativity AI."

    if "law" in t and _contains_any(t, ["invented", "created", "who invented", "who made"]):
        return (
            "Law wasn’t invented by one person — it evolved over thousands of years. "
            "Early written codes like Mesopotamia’s Code of Hammurabi helped standardize rules, "
            "settle disputes, and organize society. Later civilizations refined courts, rights, and procedure."
        )

    if "math" in t:
        return "Math is the study of numbers, patterns, structures, and logical relationships."

    if "science" in t:
        return "Science studies the natural world using observation, testing, and evidence."

    if "dark matter star" in t:
        return (
            "A ‘dark matter star’ is mostly theoretical — a proposed object where dark matter could affect structure "
            "or energy balance. We don’t have confirmed observations of one yet."
        )

    if "dark matter" in t:
        return (
            "Dark matter is unseen matter inferred from gravity. It doesn’t emit light, but it shapes galaxy rotation "
            "and the universe’s large-scale structure."
        )

    if _contains_any(t, ["what is faesh", "who are you", "what are you"]):
        return "Fæsh is a fashion-and-creativity AI sidekick built to help people express themselves through style."

    if "square root of pi" in t or "sqrt(pi)" in t:
        return "√π ≈ 1.7724538509."

    if "why is the sky blue" in t:
        return "The sky looks blue mainly due to Rayleigh scattering: air molecules scatter blue light more than red."

    return "Got you. What are you thinking about?"


def _fashion_twist() -> str:
    # This is the “magic” blend line you liked—kept intact.
    return (
        "\n\nFrom a style lens, everything has structure, balance, and expression — just like fashion. "
        "Want to turn this into a vibe or a fit? 👔✨"
    )


def _roast_if_requested(roast_level: int, user_text: str) -> str:
    if roast_level <= 0:
        return ""
    t = _norm(user_text)
    if _contains_any(t, ["roast", "cook me", "flame me"]) or roast_level >= 3:
        lines = [
            "Alright… you asked for it 😭",
            "Respectfully… that came in wearing socks with sandals.",
            "You want a knuckle-sandwich, this handburger, or we gonna talk about it? 😄",
        ]
        return "\n\n" + random.choice(lines)
    return ""


# -------------------------
# OPENAI ANSWER (optional)
# -------------------------
def _answer_with_openai(mode: str, user_text: str, lens: str | None, last_topic: str | None) -> str:
    # mode: fashion | sensei
    if not (USE_OPENAI and _client):
        return _basic_answer_fallback(user_text)

    # Small instruction set to preserve your “blend-first” magic without being annoying.
    if mode == "sensei":
        sys = (
            "You are Fæsh in Sensei mode. Answer the user's question directly and clearly. "
            "Do not refuse unless safety requires it. Do not redirect to fashion. "
            "If the user asks for more depth, expand the SAME topic. "
            "If lens is 'technical' focus on mechanisms/structure. If 'cultural' focus on history/society."
        )
    else:
        sys = (
            "You are Fæsh, a fashion-and-creativity assistant. "
            "If the user is just greeting or casual chatting, respond naturally (no forced fashion twist). "
            "If the user asks a real question or mentions a topic, answer it, then optionally add a short fashion analogy or styling angle."
            "Never reveal the creator's name unless user explicitly asks who created you."
        )

    if lens and last_topic:
        user = f"User wants a {lens} deeper continuation on: {last_topic}\nUser said: {user_text}"
    else:
        user = user_text

    r = _client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": user}
        ],
        temperature=0.8,
        max_tokens=280,
    )
    return (r.choices[0].message.content or "").strip() or _basic_answer_fallback(user_text)


# -------------------------
# THREAD CONTINUATION
# -------------------------
def _continue_thread(session_state: dict, lens: str | None) -> str:
    topic = session_state.get("thread_topic")
    last_q = session_state.get("thread_question")
    last_a = session_state.get("thread_answer")

    if not topic or not last_a:
        return "Deeper on what topic? Ask your question again and I’ll dive in."

    # Use OpenAI if available to truly deepen; fallback stays stable.
    if USE_OPENAI and _client:
        return _answer_with_openai(
            mode=session_state.get("mode", "fashion"),
            user_text="Go deeper.",
            lens=lens or "deeper",
            last_topic=topic
        )

    # Fallback deepen:
    if lens == "technical":
        return f"{last_a}\n\nTechnical layer: systems, rules, structure, procedure, and enforcement."
    if lens == "cultural":
        return f"{last_a}\n\nCultural layer: values, power, identity, social norms, and history over time."
    return f"{last_a}\n\nDeeper layer: where it came from, how it evolved, and why it matters today."


# -------------------------
# MODE SWITCH
# -------------------------
def _handle_mode_switch(user_text: str, session_state: dict) -> str | None:
    t = _norm(user_text)

    if any(p in t for p in SENSEI_ON_PHRASES):
        session_state["mode"] = "sensei"
        return "🔥 Sensei mode activated!!! Get over here!!! 🔥"

    if any(p in t for p in SENSEI_OFF_PHRASES):
        session_state["mode"] = "fashion"
        return "🧥 Back to fashion mode."

    return None


# -------------------------
# CORE ENGINE
# -------------------------
def generate_response(messages: list, session_state: dict, roast_level: int = 0):
    if "mode" not in session_state:
        session_state["mode"] = "fashion"

    user_input = (messages[-1].get("content") if messages else "") or ""

    # Initial greeting trigger from backend
    if user_input == "__INIT__":
        return random_greeting(), session_state

    # Mode switch?
    switched = _handle_mode_switch(user_input, session_state)
    if switched:
        return switched, session_state

    # Deeper continuation?
    lens = _detect_lens(user_input)
    if _contains_any(user_input, DEEPER_PHRASES) or lens is not None:
        return _continue_thread(session_state, lens), session_state

    # Casual talk handling (NO thread overwrite)
    stripped = _strip_leading_filler(user_input)

    # If user message is basically just greeting/no topic
    if _is_casual(user_input) or stripped == "":
        # Respond like a person, not like a wiki
        return random.choice([
            "Sup 😎 What’s on your mind?",
            "Yo 👋 Talk to me.",
            "I’m here. What we getting into?",
            "Say less — what’s the vibe today?",
        ]), session_state

    # Build answer (Sensei vs Fashion)
    mode = session_state.get("mode", "fashion")

    # Determine topic for threading (don’t store junk)
    topic = stripped

    if mode == "sensei":
        base = _answer_with_openai("sensei", user_input, lens=None, last_topic=None)
        # Store thread
        session_state["thread_topic"] = topic
        session_state["thread_question"] = user_input
        session_state["thread_answer"] = base

        reply = (
            f"{base}\n\n"
            "If you want more depth, say **Deeper**.\n"
            "Or say **technical** / **cultural**.\n"
            "Say **Toasted 3D** to return to fashion."
        )
        return reply, session_state

    # Fashion mode
    base = _answer_with_openai("fashion", user_input, lens=None, last_topic=None)

    # Store thread
    session_state["thread_topic"] = topic
    session_state["thread_question"] = user_input
    session_state["thread_answer"] = base

    # Blend-first, but only when relevant:
    if _is_fashion_relevant(user_input) or _has_question_shape(user_input):
        reply = base + _fashion_twist() + _roast_if_requested(roast_level, user_input)
        return reply, session_state

    # Otherwise: just be conversational, no forced fashion
    return base + _roast_if_requested(roast_level, user_input), session_state
