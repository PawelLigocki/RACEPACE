from fastapi.testclient import TestClient
import pytest
from app.api import app

client = TestClient(app)


# -----------------------------
# Test root endpoint
# -----------------------------
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "RaceCalc API"


# -----------------------------
# Test /pace endpoint (valid)
# -----------------------------
@pytest.mark.parametrize(
    "distance,time,expected_pace",
    [
        (10, 50, 5),       # standard case
        (5, 25, 5),        # same pace, smaller distance
        (12, 60, 5),       # decimal pace
    ]
)
def test_pace_valid(distance, time, expected_pace):
    response = client.get(f"/pace?distance={distance}&time={time}")
    assert response.status_code == 200
    data = response.json()
    assert "pace" in data
    assert data["pace"] == expected_pace


# -----------------------------
# Test /pace endpoint (invalid)
# -----------------------------
@pytest.mark.parametrize(
    "distance,time,expected_detail",
    [
        (0, 50, "Distance must be greater than zero"),
        (-5, 50, "Distance must be greater than zero"),
        (10, 0, "Time must be greater than zero"),
        (10, -1, "Time must be greater than zero"),
    ]
)
def test_pace_invalid(distance, time, expected_detail):
    response = client.get(f"/pace?distance={distance}&time={time}")
    assert response.status_code == 400
    assert expected_detail in response.json()["detail"]


# -----------------------------
# Test /predict endpoint (valid)
# -----------------------------
@pytest.mark.parametrize(
    "distance,time,target",
    [
        (5, 25, 10),
        (10, 50, 21),
    ]
)
def test_predict_valid(distance, time, target):
    response = client.get(f"/predict?distance={distance}&time={time}&target={target}")
    assert response.status_code == 200
    data = response.json()
    assert "predicted_time" in data
    assert data["predicted_time"] > 0


# -----------------------------
# Test /predict endpoint (invalid)
# -----------------------------
@pytest.mark.parametrize(
    "distance,time,target",
    [
        (-5, 25, 10),
        (5, -25, 10),
        (5, 25, 0),
        (5, 25, -10),
    ]
)
def test_predict_invalid(distance, time, target):
    response = client.get(f"/predict?distance={distance}&time={time}&target={target}")
    assert response.status_code == 400