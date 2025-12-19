from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
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
    messages: list
    roast_level: int = 1

@app.get("/")
def health():
    return {"status": "Faesh is alive"}

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(req.messages, req.roast_level)
    return {"reply": reply}
