from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from ai.engine import generate_response

app = FastAPI()

# -------------------------
# CORS (STABLE)
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
# CHAT ENDPOINT
# -------------------------
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()

    # Accept flexible fields from frontend
    user_message = body.get("message") or body.get("text") or body.get("input")

    if isinstance(user_message, dict):
        user_message = user_message.get("content")

    messages = body.get("messages", [])
    session_state = body.get("session_state") or {}
    roast_level = int(body.get("roast_level", body.get("roastLevel", 0)) or 0)

    # If the page just loaded and we got no message, trigger greeting safely
    if not user_message and not messages:
        messages = [{"role": "user", "content": "__INIT__"}]
    else:
        if user_message:
            messages.append({"role": "user", "content": str(user_message)})

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
