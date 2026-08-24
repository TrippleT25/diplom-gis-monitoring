from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_monitoring_object_with_invalid_latitude():
    response = client.post(
        "/monitoring-objects",
        json={
            "name": "Invalid meter",
            "latitude": 100,
            "longitude": 20,
        },
    )

    assert response.status_code == 422