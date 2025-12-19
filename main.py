from fastapi import FastAPI
from pydantic import BaseModel
from ai.engine import generate_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    roast_level: int = 1

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(req.message, req.roast_level)
    return {"reply": reply}
