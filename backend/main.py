from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from database import SessionLocal
from models import User

app = FastAPI(title="Fæsh API", version="0.1.0")

db: List[User] = []  # Dev in-memory store

class UserIn(BaseModel):
    email: str
    username: str

@app.post("/register")
def register(user: UserIn):
    for u in db:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, username=user.username)
    db.append(new_user)
    return {"message": "User registered", "user": new_user}

@app.post("/login")
def login(user: UserIn):
    for u in db:
        if u.email == user.email:
            return {"message": f"Welcome back {u.username}"}
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/health")
def health():
    return {"status": "ok"}
