from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity = "Chess Club"
    email = "student@example.edu"

    before = client.get("/activities")
    assert before.status_code == 200

    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200

    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "unregistered" in data["message"].lower()

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_missing_participant_returns_error():
    activity = "Chess Club"
    email = "not-registered@example.edu"

    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
