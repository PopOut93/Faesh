from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
        "reply": f"Faesh here 👋 You said: {user_message}"
    }
