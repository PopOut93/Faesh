from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ai.engine import generate_response

app = FastAPI()

# -------------------------
# CORS (STABLE)
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
# CHAT ENDPOINT
# -------------------------
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message") or body.get("text") or body.get("input")

    if isinstance(user_message, dict):
        user_message = user_message.get("content")

    if not user_message:
        return {"reply": "I hear you — say that again for me 🖤"}

    messages = body.get("messages", [])
    messages.append({"role": "user", "content": user_message})

    session_state = body.get("session_state", {})

    reply = generate_response(
        messages=messages,
        session_state=session_state
    )

    return {
        "reply": reply,
        "session_state": session_state
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
