from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

from ai.engine import generate_response

app = FastAPI(title="Faesh Backend")

# 🔥 THIS IS THE IMPORTANT PART
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow GitHub Pages + localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/")
def health():
    return {"status": "Faesh backend is live"}

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response([m.dict() for m in req.messages])
    return {"reply": reply}
