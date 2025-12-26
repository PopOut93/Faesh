from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from ai.engine import generate_response

app = FastAPI()

# -------------------------
# CORS (STABLE & OPEN)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
# CHAT ENDPOINT (CRASH-PROOF)
# -------------------------
@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()

        # --- Extract message safely
        user_message = (
            body.get("message")
            or body.get("text")
            or body.get("input")
        )

        if isinstance(user_message, dict):
            user_message = user_message.get("content")

        if not isinstance(user_message, str) or not user_message.strip():
            return {
                "reply": "I hear you — say that again for me 🖤",
                "session_state": {}
            }

        # --- Messages history
        messages = body.get("messages", [])
        if not isinstance(messages, list):
            messages = []

        messages.append({
            "role": "user",
            "content": user_message
        })

        # --- Session state (ALWAYS A DICT)
        session_state = body.get("session_state")
        if not isinstance(session_state, dict):
            session_state = {}

        # --- Generate reply (engine is already guarded)
        reply = generate_response(
            messages=messages,
            session_state=session_state
        )

        # --- Force safe output
        if not isinstance(reply, str):
            reply = "I’m here — try asking that again for me 🖤"

        return {
            "reply": reply,
            "session_state": session_state
        }

    except Exception:
        # 🚑 ABSOLUTE FAILSAFE — NEVER 500
        return {
            "reply": "I’m here — try asking that again for me 🖤",
            "session_state": {}
        }

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
