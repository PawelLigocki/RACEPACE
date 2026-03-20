from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "RaceCalc API"}


def test_pace_endpoint():
    response = client.get("/pace?distance=10&time=50")

    assert response.status_code == 200
    data = response.json()

    assert "pace" in data
    assert data["pace"] == 5


def test_predict_endpoint():
    response = client.get("/predict?distance=5&time=25&target=10")

    assert response.status_code == 200
    data = response.json()

    assert "predicted_time" in data
    assert data["predicted_time"] > 0

def test_pace_invalid():
    response = client.get("/pace?distance=0&time=50")

    assert response.status_code == 400
    assert "greater than zero" in response.json()["detail"]

def test_pace_invalid_distance():
    response = client.get("/pace?distance=0&time=50")

    assert response.status_code == 400
    assert "Distance" in response.json()["detail"]


def test_predict_invalid():
    response = client.get("/predict?distance=-5&time=25&target=10")

    assert response.status_code == 400