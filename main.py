from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

from ai.engine import generate_response

app = FastAPI()

# ==================================
# SIMPLE IN-MEMORY SESSION STORE
# (Persists per Render instance;
#  resets on redeploy/restart)
# ==================================
SESSIONS: dict[str, dict] = {}

def get_or_create_session(session_id: str | None) -> str:
    if not session_id:
        session_id = str(uuid4())
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "private_unlocked": False,
            "awaiting_private_passphrase": False,
            "jailin_claimed": False,
            "awaiting_jailin_realname": False,
            "legacy_unlocked": False,
        }
    return session_id

# =========================
# CORS — LOCKED & STABLE
# (No "*" to avoid weird browser behaviors)
# =========================
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

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def health():
    return {"status": "Fæsh online 🖤"}

# =========================
# CHAT — FLEXIBLE PAYLOAD + SESSION
# =========================
@app.post("/chat")
async def chat(request: Request):
    """
    Accepts ANY of the following safely:
    { message: "yo" }
    { text: "yo" }
    { input: "yo" }
    { message: { content: "yo" } }

    Session support:
    { session_id: "uuid..." }
    (If missing, backend creates it and returns it.)
    """

    # Safely parse JSON (avoid 422 if body is empty/invalid)
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    # Session
    session_id = body.get("session_id") or body.get("sessionId")
    session_id = get_or_create_session(session_id)
    session_state = SESSIONS[session_id]

    # Extract message safely
    user_message = (
        body.get("message")
        or body.get("text")
        or body.get("input")
    )

    if isinstance(user_message, dict):
        user_message = user_message.get("content")

    if not user_message or not isinstance(user_message, str):
        return {
            "reply": "I hear you — say that again for me 🖤",
            "session_id": session_id,
        }

    # Optional history (kept simple)
    messages = body.get("messages", [])
    history = []
    for m in messages:
        if isinstance(m, dict) and "role" in m and "content" in m:
            history.append({"role": m["role"], "content": str(m["content"])})

    history.append({"role": "user", "content": user_message})

    roast_level = body.get("roast_level", body.get("roastLevel", 0))
    try:
        roast_level = int(roast_level)
    except Exception:
        roast_level = 0

    reply = generate_response(
        messages=history,
        roast_level=roast_level,
        session_state=session_state
    )

    return {
        "reply": reply,
        "session_id": session_id,
        "private_unlocked": bool(session_state.get("private_unlocked")),
        "legacy_unlocked": bool(session_state.get("legacy_unlocked")),
    }

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
