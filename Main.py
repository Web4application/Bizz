from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import jwt, bcrypt, os, openai

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

class Creds(BaseModel):
    email: EmailStr
    password: str

users = {}  # in‑memory demo; swap for DB

def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def verify_pw(pw: str, hashed: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed.encode())

def issue_jwt(email: str):
    return jwt.encode({"sub": email}, JWT_SECRET, algorithm="HS256")

@app.post("/register")
def register(c: Creds):
    if c.email in users:
        raise HTTPException(400, "User exists")
    users[c.email] = hash_pw(c.password)
    return {"message": "Registered ✔️", "token": issue_jwt(c.email)}

@app.post("/login")
def login(c: Creds):
    if c.email not in users or not verify_pw(c.password, users[c.email]):
        raise HTTPException(401, "Invalid")
    return {"message": "Welcome back!", "token": issue_jwt(c.email)}

class ChatReq(BaseModel):
    message: str

@app.post("/chat")
def chat(q: ChatReq):
    if not OPENAI_KEY:
        raise HTTPException(500, "OpenAI key not set")
    openai.api_key = OPENAI_KEY
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini", messages=[{"role":"user","content":q.message}]
    )
    return {"reply": resp.choices[0].message.content.strip()}
