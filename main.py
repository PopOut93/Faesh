from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ CORS CONFIG — THIS IS THE FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",  # your frontend
        "http://localhost:5500",       # optional local testing
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(data: ChatRequest):
    user_message = data.message.strip()

    if not user_message:
        return {"reply": "Hey — say something so I can vibe with you 🙂"}

    return {
        "reply": f"Fæsh here 👋 You said: {user_message}"
    }
