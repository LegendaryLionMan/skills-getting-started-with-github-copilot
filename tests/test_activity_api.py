from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email():
    # Arrange
    activity = "Chess Club"
    email = "student@example.edu"

    # Act
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert "unregistered" in unregister_response.json()["message"].lower()
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_missing_participant_returns_error():
    # Arrange
    activity = "Chess Club"
    email = "not-registered@example.edu"

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
