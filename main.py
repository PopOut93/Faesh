from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import base64
import os

from ai.engine import generate_response

app = FastAPI(title="Faesh Backend", version="1.1.0")

# CORS (GitHub Pages + local)
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


# =========================
# MODELS
# =========================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7


# =========================
# HEALTH
# =========================

@app.get("/")
@app.head("/")
def health():
    return {"status": "Faesh backend is live"}


# =========================
# CHAT ENDPOINT
# =========================

@app.post("/chat")
def chat(req: ChatRequest):
    messages = [m.dict() for m in req.messages]
    reply = generate_response(messages, req.temperature)
    return {"reply": reply}


# =========================
# VISION ENDPOINT (IMAGE UPLOAD)
# =========================

@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Be honest and critique this outfit."},
                {"type": "input_image", "image_base64": image_b64}
            ]
        }
    ]

    reply = generate_response(messages)
    return {"reply": reply}
