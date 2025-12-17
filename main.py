from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from ai.engine import generate_response

app = FastAPI(title="Faesh Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    roast_level: int = 1

@app.get("/")
def health():
    return {"status": "Faesh backend is live"}

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(
        [m.dict() for m in req.messages],
        roast_level=req.roast_level
    )
    return {"reply": reply}

@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {
        "analysis": f"Faesh received image: {file.filename}. Vision analysis coming soon."
    }
