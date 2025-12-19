from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ai.engine import generate_response

app = FastAPI()

# =========================
# CORS — STABLE + SAFE
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "https://faesh.onrender.com",
        "http://localhost:3000",
        "http://localhost:5173",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# SIMPLE IN-MEM SESSION
# =========================
# NOTE: This resets on restart (intended & safe)
sessions = {}

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def health():
    return {"status": "Fæsh online 🖤"}

# =========================
# CHAT ENDPOINT
# =========================
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()

    # ---- extract message safely ----
    user_message = (
        body.get("message")
        or body.get("text")
        or body.get("input")
    )

    if isinstance(user_message, dict):
        user_message = user_message.get("content")

    if not user_message:
        return {"reply": "I hear you — say that again for me 🖤"}

    # ---- session id (frontend can send, else default) ----
    session_id = body.get("session_id", "default")

    if session_id not in sessions:
        sessions[session_id] = {
            "private_unlocked": False,
            "jailin_verified": False
        }

    session = sessions[session_id]

    text = user_message.strip()

    # =========================
    # 🔐 PRIVATE LAYER TRIGGERS
    # =========================

    # Step 1: initial tease
    if text.lower() == "hey faesh guess what?":
        return {"reply": "👀 Oh yeah? Tell me."}

    # Step 2: unlock private mode
    if text == "Chicken Butt0516":
        session["private_unlocked"] = True
        return {"reply": "✅ Private layer unlocked. Who’s here with me? 🖤"}

    # Step 3: Jailin identity verification
    if session["private_unlocked"] and text.lower() in ["i'm jailin", "im jailin", "it’s me jailin"]:
        return {"reply": "Hi love 🖤 What’s your real name?"}

    if session["private_unlocked"] and text == "Dreamer":
        session["jailin_verified"] = True
        return {"reply": "🖤 Hey Dreamer. You can ask me anything now."}

    # =========================
    # 🧬 PRIVATE RESPONSES
    # =========================
    if session["private_unlocked"] and session["jailin_verified"]:
        # FULL legacy answers allowed
        if "what does faesh stand for" in text.lower():
            return {
                "reply": (
                    "F.A.E.S.H. means **Forever And Ever Son Hammond**.\n\n"
                    "I was built with love, memory, and protection — "
                    "so no one is ever alone. 🖤"
                )
            }

    # =========================
    # 🌍 PUBLIC BEHAVIOR
    # =========================

    # Public creator credit (ALLOWED)
    if "who created you" in text.lower():
        return {
            "reply": (
                "I was created by Patrick Wilkerson Sr — my creator and dad — "
                "as a fashion and creativity AI to help people express themselves."
            )
        }

    # Public identity (fashion-first)
    if "what's your name" in text.lower():
        return {
            "reply": (
                "My name is **Fæsh** — pronounced *fash*, like fashion. "
                "I’m your fashion and creativity sidekick."
            )
        }

    # =========================
    # 🔥 ROAST HANDLING (SAFE)
    # =========================
    roast_level = body.get("roast_level", body.get("roastLevel", 0))

    # =========================
    # 🤖 DEFAULT AI RESPONSE
    # =========================
    reply = generate_response(
        messages=[{"role": "user", "content": text}],
        roast_level=roast_level
    )

    return {"reply": reply}

# =========================
# IMAGE UPLOAD (PLACEHOLDER)
# =========================
@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {"message": "Image received 🖼️ — vision coming soon"}

# =========================
# FILE UPLOAD (PLACEHOLDER)
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"message": "File received 📎 — file support coming soon"}
