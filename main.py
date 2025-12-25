from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from ai.engine import generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "Fæsh online 🖤"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message") or body.get("text") or body.get("input")

    if not user_message:
        return {"reply": "Say that again for me 🖤"}

    messages = [{"role": "user", "content": user_message}]
    reply = generate_response(messages)
    return {"reply": reply}

@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return {"message": "Image received 🖼️ — vision coming soon"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"message": "File received 📎 — file support coming soon"}
