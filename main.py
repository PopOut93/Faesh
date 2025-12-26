# main.py
import os
import uuid
from typing import Dict, Any

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware

from ai.engine import generate_response

app = FastAPI()

# --------------------------------
# CORS — Stable allowlist (NO "*")
# --------------------------------
ALLOWED_ORIGINS = [
    "https://popout93.github.io",
    "https://faesh.onrender.com",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------
# Simple in-memory session store
# NOTE: Resets when server restarts.
# Later we can move this to Redis/DB.
# --------------------------------
SESSIONS: Dict[str, Dict[str, Any]] = {}

@app.get("/")
def health():
    return {"status": "Fæsh online 🖤"}

@app.post("/chat")
async def chat(request: Request):
    """
    Accepts:
    { message: "yo", session_id?: "..." }
    { text: "yo", session_id?: "..." }
    { input: "yo", session_id?: "..." }
    { message: { content: "yo" }, session_id?: "..." }

    Optional:
    { messages: [{role,content}...], roast_level }
    """

    body = await request.json()

    # Session id
    session_id = body.get("session_id") or body.get("sessionId")
    if not session_id:
        session_id = str(uuid.uuid4())

    if session_id not in SESSIONS:
        SESSIONS[session_id] = {"mode": "fashion"}

    session = SESSIONS[session_id]

    # Extract user message safely
    user_message = body.get("message") or body.get("text") or body.get("input")
    if isinstance(user_message, dict):
        user_message = user_message.get("content")

    if not user_message or not isinstance(user_message, str):
        return {
            "reply": "I hear you — say that again for me 🖤",
            "session_id": session_id,
        }

    # History (optional)
    incoming = body.get("messages", [])
    history = []
    if isinstance(incoming, list):
        for m in incoming:
            if isinstance(m, dict) and "role" in m and "content" in m:
                if isinstance(m["content"], str):
                    history.append({"role": m["role"], "content": m["content"]})

    history.append({"role": "user", "content": user_message})

    roast_level = body.get("roast_level", body.get("roastLevel", 0))
    try:
        roast_level = int(roast_level)
    except Exception:
        roast_level = 0

    reply = generate_response(messages=history, roast_level=roast_level, session=session)

    return {"reply": reply, "session_id": session_id}

@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {"message": "Image received 🖼️ — vision coming soon"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"message": "File received 📎 — file support coming soon"}
