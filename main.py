from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: list
    roast_level: int = 1

@app.post("/chat")
async def chat(req: ChatRequest):
    return {
        "reply": f"Faesh received: {req.messages[-1]['content']}"
    }
