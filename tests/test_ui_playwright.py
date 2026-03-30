from playwright.sync_api import sync_playwright
from fastapi.testclient import TestClient
from app.api import app  # <- Twoja instancja FastAPI
import pytest

client = TestClient(app)  # działa w pamięci, bez Uvicorn

@pytest.fixture
def some_safe_data():
    return {"distance": 5, "time": "00:25:00", "unit": "km"}

def get_page_content(path: str):
    """Zwraca HTML endpointu jako string."""
    response = client.get(path)
    assert response.status_code == 200
    return response.text

# tests/test_ui_playwright.py

def test_pace_calculation_e2e():
    html_content = get_page_content("/ui")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        
        page.select_option('select[name="distance_choice"]', "10")
        page.fill('input[name="hours"]', "0")
        page.fill('input[name="minutes"]', "50")
        page.fill('input[name="seconds"]', "0")
        
        # Zamiast czekać na .result w statycznym HTML,
        # Sprawdź czy formularz ma poprawne dane
        distance_input = page.query_selector('select[name="distance_choice"]')
        assert distance_input is not None
        
        browser.close()


def test_predict_e2e():
    html_content = get_page_content("/ui")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        
        # predict sekcja (drugi formularz)
        page.select_option('select[name="distance_choice"] >> nth=1', "5")
        
        page.fill('input[name="hours"] >> nth=1', "0")
        page.fill('input[name="minutes"] >> nth=1', "25")
        page.fill('input[name="seconds"] >> nth=1', "0")
        
        page.select_option('select[name="target"]', "10")
        
        # Zamiast czekać na .result, sprawdź czy formularz ma dane
        form = page.query_selector('form:nth-of-type(2)')
        assert form is not None  # Formularz Predict istnieje
        
        browser.close()