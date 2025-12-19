from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ CORS — DO NOT TOUCH (this is correct now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "http://localhost:5500",
        "http://localhost:3000",
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
    user_message = data.message.strip().lower()

    if not user_message:
        return {"reply": "Hey — say something so I can vibe with you 🙂"}

    # ✅ INTENT HANDLING (START)
    if "who created you" in user_message or "who greated you" in user_message:
        return {
            "reply": "I was created by Patrick Wilkerson Sr — my creator and father."
        }

    # default fallback (echo, friendly)
    return {
        "reply": f"Fæsh here 👋 You said: {data.message}"
    }
