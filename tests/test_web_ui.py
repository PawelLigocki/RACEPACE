from fastapi.testclient import TestClient
from app.api import app
from bs4 import BeautifulSoup

client = TestClient(app)


def test_ui_page_loads():
    response = client.get("/ui")
    
    # sprawdź status
    assert response.status_code == 200

    # parsowanie HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # sprawdź np. czy strona zawiera element <form>
    assert soup.find("form") is not None


def test_ui_contains_forms():
    response = client.get("/ui")

    soup = BeautifulSoup(response.text, "html.parser")

    forms = soup.find_all("form")

    assert len(forms) >= 2

def test_ui_pace_flow():
    response = client.get("/pace-ui?distance=10&time=50")
    assert response.status_code == 200

    # Parsowanie HTML zamiast JSON
    soup = BeautifulSoup(response.text, "html.parser")
    pace_text = soup.find("p", string=lambda x: x and "Pace:" in x).text
    assert "5.0" in pace_text

def test_ui_result_display():
    response = client.get("/pace-ui?distance=10&time=50")

    assert response.status_code == 200
    assert "Pace" in response.text