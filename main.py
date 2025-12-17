from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

from ai.engine import generate_response, analyze_fashion_image, summarize_uploaded_text_file

app = FastAPI(title="Faesh Backend", version="1.0.0")

# ✅ CORS: allow GitHub Pages + local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://popout93.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: List[Dict]
    roast_level: Optional[int] = 1

@app.get("/")
def health():
    return {"status": "Faesh is alive"}

@app.post("/chat")
def chat(req: ChatRequest):
    reply = generate_response(req.messages, req.roast_level or 1)
    return {"reply": reply}

@app.post("/vision")
async def vision(
    image: UploadFile = File(...),
    prompt: str = Form(""),
    roast_level: int = Form(1),
):
    img_bytes = await image.read()
    reply = analyze_fashion_image(img_bytes, prompt=prompt, roast_level=roast_level)
    return {"reply": reply, "filename": image.filename}

@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    purpose: str = Form("Summarize this and suggest improvements."),
):
    data = await file.read()

    # Try decode as text (best-effort)
    text = ""
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        text = ""

    if not text.strip():
        return {
            "reply": "File received. I can analyze text-based files best right now (txt/csv/json). "
                    "For PDFs/Docx, we’ll add parsing next.",
            "filename": file.filename
        }

    reply = summarize_uploaded_text_file(text=text, roast_level=0, purpose_hint=purpose)
    return {"reply": reply, "filename": file.filename}
