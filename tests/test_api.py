import os, pytest, json
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)
API_KEY = {"X-API-Key": os.getenv("API_KEY", "change-me")}

def test_health():
    r = client.get("/api/health")
    assert r.json() == {"status": "ok"}

def test_chat_requires_key():
    r = client.post("/api/assistant/chat", json={"message": "Hi"}, headers={})
    assert r.status_code == 422  # missing header

def test_chat_flow():
    r = client.post("/api/assistant/chat", json={"message": "Hello!"}, headers=API_KEY)
    assert r.status_code == 200
    data = r.json()
    assert "response" in data and "memory" in data
