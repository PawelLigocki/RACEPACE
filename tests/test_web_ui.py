from fastapi.testclient import TestClient
from app.api import app
from bs4 import BeautifulSoup

client = TestClient(app)


def test_ui_page_loads():
    response = client.get("/ui")

    assert response.status_code == 200

    soup = BeautifulSoup(response.text, "html.parser")

    assert soup.find("h1").text == "Race Calculator"
    assert soup.find("form") is not None


def test_ui_contains_forms():
    response = client.get("/ui")

    soup = BeautifulSoup(response.text, "html.parser")

    forms = soup.find_all("form")

    assert len(forms) >= 2

def test_ui_pace_flow():
    response = client.get("/pace-ui?distance=10&time=50")

    assert response.status_code == 200
    assert response.json()["pace"] == 5

def test_ui_result_display():
    response = client.get("/pace-ui?distance=10&time=50")

    assert response.status_code == 200
    assert "Pace" in response.text