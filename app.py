import os
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import openai
from database import SessionLocal, engine, Base
from models import User, ChatMessage

# Load .env config
from dotenv import load_dotenv
load_dotenv()

# OpenAI config
openai.api_key = os.getenv("OPENAI_API_KEY")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4")

# JWT config
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# API key config (legacy for some endpoints)
API_KEY = os.getenv("API_KEY", "change-me")

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bizz API with Auth & GPT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models for requests/responses
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    history: List[Dict[str, str]]

# Auth utils
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

# Legacy API key dependency
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# Routes

# Registration
@app.post("/api/auth/register", response_model=UserOut, tags=["auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login
@app.post("/api/auth/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# GPT Chat
@app.post("/api/assistant/chat", response_model=ChatResponse, tags=["assistant"])
def chat_gpt(req: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Load last 10 chat messages
    history_db = db.query(ChatMessage).filter(ChatMessage.user_id == user.id).order_by(ChatMessage.timestamp.desc()).limit(10).all()
    history_db.reverse()
    messages = [{"role": m.role, "content": m.content} for m in history_db]
    messages.append({"role": "user", "content": req.message})

    try:
        res = openai.ChatCompletion.create(model=GPT_MODEL, messages=messages)
        reply = res.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save user message & assistant reply to DB
    db.add(ChatMessage(user_id=user.id, role="user", content=req.message))
    db.add(ChatMessage(user_id=user.id, role="assistant", content=reply))
    db.commit()

    # Return last 10 messages including new
    full_history = db.query(ChatMessage).filter(ChatMessage.user_id == user.id).order_by(ChatMessage.timestamp.desc()).limit(10).all()
    full_history.reverse()
    out_history = [{"role": m.role, "content": m.content} for m in full_history]

    return {"response": reply, "history": out_history}

# File upload
class UploadPayload(BaseModel):
    filename: str
    content: str

@app.post("/api/data/upload", tags=["data"], dependencies=[Depends(verify_api_key)])
def upload(data: UploadPayload):
    if not data.content:
        raise HTTPException(status_code=400, detail="Empty content")
    return {"status": "received", "filename": data.filename}

# Health
@app.get("/api/health", tags=["misc"])
def health():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to Bizz API with Auth & GPT"}
