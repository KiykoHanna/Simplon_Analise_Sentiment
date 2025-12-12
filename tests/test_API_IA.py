import sys
import os

from fastapi.testclient import TestClient
from API_IA.fastapi_IA import app

client = TestClient(app)

def test_root():
    payload = {"texte": "Test sentiment analyse"}
    response = client.post("/analyse/", json=payload)
    assert response.status_code == 200
