from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from ai.engine import generate_response

app = FastAPI()

# =========================
# CORS (FIXED)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CHAT ENDPOINT
# =========================

@app.post("/chat")
async def chat(
    message: str = Form(...),
    roast_level: int = Form(1)
):
    messages = [{"role": "user", "content": message}]
    reply = generate_response(messages, roast_level)
    return {"response": reply}

# =========================
# FILE UPLOAD PLACEHOLDER
# =========================

@app.post("/upload")
async def upload(file: UploadFile):
    return {"filename": file.filename}
