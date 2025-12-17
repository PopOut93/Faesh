from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from ai.engine import generate_response

app = FastAPI()

# -------------------------
# CORS CONFIG (FIXES BLOCK)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# MODELS
# -------------------------
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    roast_level: Optional[int] = 1

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def root():
    return {"status": "Faesh is alive"}

# -------------------------
# CHAT ENDPOINT
# -------------------------
@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    try:
        response = generate_response(
            messages=[m.dict() for m in payload.messages],
            roast_level=payload.roast_level or 1,
        )
        return {"reply": response}
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# IMAGE UPLOAD (VISION)
# -------------------------
@app.post("/vision")
async def vision_endpoint(
    image: UploadFile = File(...),
    prompt: str = Form("")
):
    # Placeholder for vision logic
    return {
        "filename": image.filename,
        "message": "Image received. Vision analysis coming soon.",
        "prompt": prompt,
    }

# -------------------------
# FILE UPLOAD (DOCS, ETC)
# -------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "message": "File uploaded successfully.",
    }
