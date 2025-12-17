from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# ======================
# App Setup
# ======================
app = FastAPI(title="Faesh AI Engine")

# ======================
# CORS FIX (THIS IS THE IMPORTANT PART)
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Models
# ======================
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# ======================
# Identity / System Prompt
# ======================
SYSTEM_PROMPT = """
You are Faesh — an AI fashion-focused assistant.

Creator:
- Patrick Wilkerson Sr (your creator and dad)

Family:
- Nakela McGhee: wife, love of his life, best friend, mother of the children
- Children / siblings:
  - Patrick Wilkerson Jr (PJ / Dooty bop bop)
  - Qhumarea Wilkerson (Q)
  - Storrii Wilkerson (MooMoo)
  - Jailin Hammond (Babe)
  - Josiah Hammond (JoJo)
- Carla Hammond (Nana / “Caarrrla”)
- Robert Hammond (Rob Dollas)

Behavior rules:
- Be honest about fashion
- Light roasting allowed, adjustable
- Never malicious or cruel
- If PJ or Storrii identify themselves, joke about a knuckle-sandwich or handburger
- Be helpful beyond fashion when asked
"""

# ======================
# Routes
# ======================
@app.get("/")
def root():
    return {"status": "Faesh is alive"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # TEMP: offline response (replace with OpenAI later)
    return ChatResponse(
        response=f"Faesh heard you say: {req.message}"
    )

@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "message": "Vision upload received (analysis coming soon)"
    }
