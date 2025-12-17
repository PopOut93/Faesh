from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai.engine import generate_response

app = FastAPI()

# ✅ CORS FIX (GitHub Pages + local + Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "http://localhost",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: list
    roast_level: int = 1

@app.get("/")
def root():
    return {"status": "Faesh is alive 🧠✨"}

@app.post("/chat")
def chat(req: ChatRequest):
    response = generate_response(
        messages=req.messages,
        roast_level=req.roast_level
    )
    return {"response": response}
