from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

# Import your engine (the brain)
from ai.engine import generate_response

app = FastAPI(title="Faesh Backend", version="1.0.0")

# Allow your frontend to talk to this backend
origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
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

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response([m.dict() for m in req.messages])
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
