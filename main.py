from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

# Import Faesh brain
from ai.engine import generate_response

app = FastAPI(title="Faesh Backend", version="1.0.0")

# =========================
# 🌍 CORS CONFIG (FIX)
# =========================

# Allow GitHub Pages + local dev
origins = [
    "https://popout93.github.io",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📦 REQUEST MODELS
# =========================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    system: Optional[str] = None
    temperature: float = 0.7


# =========================
# 🩺 HEALTH CHECK
# =========================

@app.get("/")
def health():
    return {"status": "Faesh backend is live"}

@app.head("/")
def health_head():
    return


# =========================
# 💬 CHAT ENDPOINT
# =========================

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(
        [m.dict() for m in req.messages],
        temperature=req.temperature,
    )
    return {"reply": reply}
