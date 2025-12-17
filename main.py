from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from ai.engine import generate_response

app = FastAPI(title="Faesh Backend", version="1.0.0")

# ================================
# CORS (GitHub Pages + Local)
# ================================

origins = [
    "http://localhost:3000",
    "https://popout93.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# Models
# ================================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    roast_level: Optional[int] = 1

# ================================
# Routes
# ================================

@app.get("/")
def health():
    return {"status": "Faesh backend is live"}

@app.head("/")
def health_head():
    return

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(
        [m.model_dump() for m in req.messages],
        roast_level=req.roast_level or 1
    )
    return {"reply": reply}

@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "message": "Image received. Vision analysis coming soon."
    }
