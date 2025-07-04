# FastAPI backend with:
# - JWT user registration & login
# - Assistant chat using OpenAI GPT
# - File upload
# - Health check
# - API key protected routes

import os
import openai
from typing import List, Dict
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------
SECRET_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im55YXRhZHNmcmh0YmZ4Zm55bGR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwNjY2NzYsImV4cCI6MjA2MDY0MjY3Nn0.xzUU-pmZlrTO-6-TzQu6M3eM_SeSTdjDNIHEiRtPj3Y", "super-secret")
API_KEY = os.getenv("AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10", "change-me")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------------------------------
# APP SETUP
# ----------------------------------------------------
app = FastAPI(title="Bizz API", description="GPT Assistant + Auth", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# AUTH & JWT
# ----------------------------------------------------
USERS = {"admin@example.com": {"password": "admin123"}}  # In-memory user DB

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User(BaseModel):
    email: str

class RegisterForm(BaseModel):
    email: str
    password: str


def create_access_token(data: dict, expires_delta=timedelta(hours=2)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return User(email=payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ----------------------------------------------------
# ROUTES: Auth
# ----------------------------------------------------
@app.post("/api/auth/register", tags=["auth"])
def register(user: RegisterForm):
    if user.email in USERS:
        raise HTTPException(status_code=409, detail="User already exists")
    USERS[user.email] = {"password": user.password}
    return {"message": "User registered"}


@app.post("/api/auth/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# ----------------------------------------------------
# API Key Guard
# ----------------------------------------------------
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# ----------------------------------------------------
# GPT Assistant
# ----------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

@app.post("/api/assistant/chat", tags=["assistant"], dependencies=[Depends(verify_api_key)])
def chat_gpt(req: ChatRequest):
    messages = req.history + [{"role": "user", "content": req.message}]
    try:
        res = openai.ChatCompletion.create(model=GPT_MODEL, messages=messages)
        reply = res.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return {"response": reply, "history": messages[-10:]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------------------------------
# File Upload
# ----------------------------------------------------
class UploadPayload(BaseModel):
    filename: str
    content: str

@app.post("/api/data/upload", tags=["data"], dependencies=[Depends(verify_api_key)])
def upload(data: UploadPayload):
    if not data.content:
        raise HTTPException(status_code=400, detail="Empty content")
    return {"status": "received", "filename": data.filename}

# ----------------------------------------------------
# Misc
# ----------------------------------------------------
@app.get("/api/health", tags=["misc"])
def health():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to Bizz API v1.1"}

