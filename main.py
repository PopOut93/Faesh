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
# CHAT — FLEXIBLE PAYLOAD
# =========================
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()

    # Extract message safely
    user_message = (
        body.get("message")
        or body.get("text")
        or body.get("input")
    )

    if isinstance(user_message, dict):
        user_message = user_message.get("content")

    if not user_message:
        return {"reply": "I hear you — say that again for me 🖤"}

    # Optional history
    messages = body.get("messages", [])

    history = []
    for m in messages:
        if isinstance(m, dict) and "role" in m and "content" in m:
            history.append({"role": m["role"], "content": m["content"]})

    history.append({"role": "user", "content": user_message})

    roast_level = body.get("roast_level", body.get("roastLevel", 0))

    # ✅ Stable session id per visitor (IP + user-agent)
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    session_id = f"{ip}|{ua}"

    reply = generate_response(
        messages=history,
        roast_level=roast_level,
        session_id=session_id,
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
