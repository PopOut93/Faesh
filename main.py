from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai.engine import generate_response

app = FastAPI()

# =========================
# 🌍 CORS (STABLE + FINAL)
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "https://faesh.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📩 REQUEST MODEL
# =========================

class ChatRequest(BaseModel):
    messages: list
    roast_level: int = 1

# =========================
# 💬 CHAT ENDPOINT
# =========================

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(
        messages=req.messages,
        roast_level=req.roast_level
    )
    return {"reply": reply}

# =========================
# 🫀 HEALTH CHECK
# =========================

@app.get("/")
def root():
    return {"status": "Faesh is alive"}
