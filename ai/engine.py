from __future__ import annotations

import os
from typing import Any, Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ---------------------------
# App
# ---------------------------
app = FastAPI(title="Faesh Backend", version="1.0.0")


# ---------------------------
# CORS (so your frontend can call this API)
# ---------------------------
# For production: set FRONTEND_ORIGINS in Render env vars (comma-separated).
# Example:
# FRONTEND_ORIGINS=https://your-frontend.onrender.com,http://localhost:3000
origins_env = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# Request / Response models
# ---------------------------
Role = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    system: Optional[str] = None
    temperature: float = 0.7


class ChatResponse(BaseModel):
    reply: str


# ---------------------------
# Engine hookup
# ---------------------------
def generate_reply(messages: List[Message], system: Optional[str], temperature: float) -> str:
    """
    PRODUCTION HOOK:
    Replace this with your real engine call.

    Example patterns you might swap in later:
      - from engine import generate_response
      - return generate_response([...])

    For now, this is a safe "echo bot" so the whole pipeline works.
    """
    # Find last user message
    last_user = ""
    for m in reversed(messages):
        if m.role == "user":
            last_user = m.content
            break

    if not last_user:
        return "Faesh GodBot: Send me a message and I’ll respond."

    # Simple response (placeholder)
    return f"Faesh GodBot heard you say: {last_user}"


# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def health() -> Dict[str, Any]:
    return {"status": "Faesh backend is live", "docs": "/docs"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    try:
        reply = generate_reply(req.messages, req.system, req.temperature)
        return ChatResponse(reply=reply)
    except Exception as e:
        # Don’t leak internals; log in Render logs instead if needed
        raise HTTPException(status_code=500, detail="Chat failed") from e


# ---------------------------
# Local dev entrypoint (optional)
# Render usually runs uvicorn itself via Start Command.
# ---------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "10000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
