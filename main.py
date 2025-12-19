from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import the Faesh engine (already deployed successfully)
from ai.engine import generate_response

app = FastAPI()

# =========================
# CORS — PERMANENT FIX
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "https://faesh.onrender.com",
        "http://localhost:3000",
        "http://localhost:5173",
        "*",  # safe here because no auth + no cookies
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODELS
# =========================
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    messages: Optional[List[ChatMessage]] = []
    roast_level: Optional[int] = 0

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def health():
    return {"status": "Faesh online 🖤"}

# =========================
# CHAT ENDPOINT (REAL ENGINE)
# =========================
@app.post("/chat")
def chat(request: ChatRequest):
    """
    Accepts:
    {
      message: "yo",
      messages: [...],
      roast_level: 0-5
    }
    """

    # Build conversation history safely
    history = []

    if request.messages:
        for m in request.messages:
            history.append({"role": m.role, "content": m.content})

    # Append the new user message
    history.append({"role": "user", "content": request.message})

    # Call the REAL Faesh engine
    response_text = generate_response(
        messages=history,
        roast_level=request.roast_level or 0,
    )

    return {
        "reply": response_text
    }

# =========================
# IMAGE UPLOAD (SAFE STUB)
# =========================
@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {
        "message": "Image received 🖼️ — vision analysis coming soon"
    }

# =========================
# FILE UPLOAD (SAFE STUB)
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {
        "message": "File received 📎 — file analysis coming soon"
    }
