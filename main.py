from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ai.engine import generate_response

app = FastAPI()

# =========================
# 🔐 HARD CORS LOCK (RENDER SAFE)
# =========================
ALLOWED_ORIGINS = [
    "https://popout93.github.io",
    "https://faesh.onrender.com",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
async def health():
    return JSONResponse(
        content={"status": "Fæsh online 🖤"},
        headers={"Access-Control-Allow-Origin": "*"},
    )

# =========================
# CHAT ENDPOINT (CORS SAFE)
# =========================
@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()

        user_message = (
            body.get("message")
            or body.get("text")
            or body.get("input")
        )

        if isinstance(user_message, dict):
            user_message = user_message.get("content")

        if not user_message:
            reply = "I hear you. Say that again for me 🖤"
        else:
            messages = body.get("messages", [])
            history = []

            for m in messages:
                if isinstance(m, dict) and "role" in m and "content" in m:
                    history.append(
                        {"role": m["role"], "content": m["content"]}
                    )

            history.append({"role": "user", "content": user_message})

            roast_level = body.get("roast_level", body.get("roastLevel", 0))

            reply = generate_response(
                messages=history,
                roast_level=roast_level,
            )

        return JSONResponse(
            content={"reply": reply},
            headers={
                "Access-Control-Allow-Origin": "https://popout93.github.io"
            },
        )

    except Exception as e:
        return JSONResponse(
            content={"reply": "⚠️ Faesh froze — backend error."},
            headers={
                "Access-Control-Allow-Origin": "https://popout93.github.io"
            },
            status_code=500,
        )

# =========================
# IMAGE UPLOAD (SAFE)
# =========================
@app.post("/vision")
async def vision(file: UploadFile = File(...)):
    return JSONResponse(
        content={"message": "Image received 🖼️ — vision coming soon"},
        headers={"Access-Control-Allow-Origin": "*"},
    )

# =========================
# FILE UPLOAD (SAFE)
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return JSONResponse(
        content={"message": "File received 📎 — file support coming soon"},
        headers={"Access-Control-Allow-Origin": "*"},
    )
