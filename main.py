from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import your engine (the brain)
from ai.engine import generate_response

app = FastAPI(title="Faesh Backend", version="1.0.0")

# ✅ CORS FIX — allow GitHub Pages and any frontend (safe for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all origins
    allow_credentials=False,      # must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    system: Optional[str] = None
    temperature: float = 0.7


@app.get("/")
def health():
    return {"status": "Faesh backend is live"}


@app.head("/")
def health_head():
    return


@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response([m.dict() for m in req.messages])
    return {"reply": reply}


@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response([m.dict() for m in req.messages])
    return {"reply": reply}
