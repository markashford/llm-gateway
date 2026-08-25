import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.providers.groq_client import GroqClient

client = TestClient(app)

def test_chat_endpoint_success(monkeypatch):
    # Patch the GroqClient.chat method to avoid real API calls
    async def fake_chat(self, req):
        from app.providers.interfaces import ChatResponse
        return ChatResponse(content="Hello!", model="llama-3.1-8b-instant", usage={})
    monkeypatch.setattr(GroqClient, "chat", fake_chat)

    payload = {
        "provider": "groq",
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "Hi"}],
        "temperature": 0.7,
        "max_tokens": 25
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    assert response.json()["content"] == "Hello!"

def test_chat_endpoint_invalid_provider():
    payload = {
        "provider": "invalid",
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "Hi"}],
        "temperature": 0.7,
        "max_tokens": 25
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 400


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_providers():
    response = client.get("/providers")
    assert response.status_code == 200
    assert "groq" in response.json()["providers"]