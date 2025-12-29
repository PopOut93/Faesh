from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from ai.engine import generate_response, random_greeting

app = FastAPI()

# -------------------------
# CORS (LOCKED + CORRECT)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "https://faesh.onrender.com",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def health():
    return {"status": "Fæsh online 🖤"}

# -------------------------
# GREETING (FRONTEND CALLS THIS ON LOAD)
# -------------------------
@app.get("/greet")
def greet():
    # This greeting is PUBLIC. No creator name here.
    return {"reply": random_greeting()}

# -------------------------
# CHAT ENDPOINT
# -------------------------
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()

    user_message = body.get("message") or body.get("text") or body.get("input")
    if isinstance(user_message, dict):
        user_message = user_message.get("content")

    if not user_message or not str(user_message).strip():
        return {"reply": "I hear you — say that again for me 🖤", "session_state": body.get("session_state", {})}

    messages = body.get("messages", [])
    if not isinstance(messages, list):
        messages = []

    # Ensure last user message exists in history
    messages.append({"role": "user", "content": str(user_message).strip()})

    session_state = body.get("session_state") or {}
    if not isinstance(session_state, dict):
        session_state = {}

    roast_level = body.get("roast_level", body.get("roastLevel", 0))
    try:
        roast_level = int(roast_level)
    except Exception:
        roast_level = 0

    reply, session_state = generate_response(
        messages=messages,
        session_state=session_state,
        roast_level=roast_level
    )

    return {"reply": reply, "session_state": session_state}

# -------------------------
# IMAGE UPLOAD (SAFE STUB)
# -------------------------
@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {"message": "🖼️ Image received — fashion vision coming soon"}

# -------------------------
# FILE UPLOAD (SAFE STUB)
# -------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"message": "📎 File received — creative tools coming soon"}
