from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from ai.engine import generate_response

app = FastAPI(title="Faesh Backend", version="1.0.0")

# --- CORS ---
origins = os.getenv(
    "FRONTEND_ORIGINS",
    "https://popout93.github.io,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    system: Optional[str] = None
    temperature: float = 0.7
    roast_level: Optional[int] = 1  # 👈 FIX (NEW)

# --- Routes ---
@app.get("/")
def health():
    return {"status": "Faesh backend is live"}

@app.head("/")
def health_head():
    return

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(
        [m.dict() for m in req.messages],
        roast_level=req.roast_level
    )
    return {"reply": reply}
