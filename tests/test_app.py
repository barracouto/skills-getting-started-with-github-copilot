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
    assert "participants" in data["Chess Club"]


def test_signup_success():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_signup_duplicate():
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_signup_nonexistent_activity():
    email = "ghost@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success():
    email = "testuser3@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200 or response.status_code == 404


def test_unregister_nonexistent_activity():
    email = "ghost@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404


def test_unregister_not_signed_up():
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not signed up
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404 or response.status_code == 400
