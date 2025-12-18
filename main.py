from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai.engine import generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    roast_level: int = 1

@app.post("/chat")
async def chat(req: ChatRequest):
    reply = generate_response(
        user_message=req.message,
        roast_level=req.roast_level
    )
    return {"reply": reply}
