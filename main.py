from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware

from ai.engine import generate_response

app = FastAPI()

# =========================
# CORS — LOCKED & STABLE
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
# HEALTH CHECK
# =========================
@app.get("/")
def health():
    return {"status": "Fæsh online 🖤"}

# =========================
# CHAT — FLEXIBLE + BULLETPROOF
# =========================
@app.post("/chat")
async def chat(request: Request):
    """
    Accepts ALL of the following safely:
    - JSON: { message: "yo" }
    - JSON: { text: "yo" }
    - JSON: { input: "yo" }
    - JSON: { message: { content: "yo" } }
    - Raw text: "yo"
    """

    user_message = None
    messages = []
    roast_level = 0

    # 1️⃣ Try JSON body first
    try:
        body = await request.json()
        if isinstance(body, dict):
            user_message = (
                body.get("message")
                or body.get("text")
                or body.get("input")
            )

            if isinstance(user_message, dict):
                user_message = user_message.get("content")

            messages = body.get("messages", [])
            roast_level = body.get("roast_level", body.get("roastLevel", 0))
    except:
        pass

    # 2️⃣ Fallback: raw text (text/plain)
    if not user_message:
        try:
            raw = await request.body()
            raw_text = raw.decode("utf-8").strip()
            if raw_text:
                user_message = raw_text
        except:
            pass

    # 3️⃣ Still nothing? gentle fallback
    if not user_message:
        return {"reply": "I hear you — say that again for me 🖤"}

    # Build conversation history safely
    history = []
    for m in messages:
        if isinstance(m, dict) and "role" in m and "content" in m:
            history.append({"role": m["role"], "content": m["content"]})

    history.append({"role": "user", "content": user_message})

    reply = generate_response(
        messages=history,
        roast_level=roast_level
    )

    return {"reply": reply}

# =========================
# IMAGE UPLOAD (SAFE)
# =========================
@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {"message": "Image received 🖼️ — vision coming soon"}

# =========================
# FILE UPLOAD (SAFE)
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"message": "File received 📎 — file support coming soon"}
