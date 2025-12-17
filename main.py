from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from ai.engine import generate_response

app = FastAPI()

# =========================
# CORS (CRITICAL FIX)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
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
    roast_level: Optional[int] = 1

# =========================
# ROUTES
# =========================
@app.get("/")
def root():
    return {"status": "Faesh is alive"}

@app.post("/chat")
async def chat(request: ChatRequest):
    response = generate_response(
        messages=[m.model_dump() for m in request.messages],
        roast_level=request.roast_level,
    )
    return {"response": response}
