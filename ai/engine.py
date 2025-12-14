from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {"status": "Faesh backend is live"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
