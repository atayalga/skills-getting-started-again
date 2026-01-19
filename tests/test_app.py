import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Chess%20Club/signup?email=test2@example.com")
    # Then unregister
    response = client.delete("/activities/Chess%20Club/unregister?email=test2@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=test@example.com")
    assert response.status_code == 404

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/unregister?email=notsigned@example.com")
    assert response.status_code == 400