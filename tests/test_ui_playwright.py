from playwright.sync_api import sync_playwright
from fastapi.testclient import TestClient
from app.api import app  # <- Twoja instancja FastAPI

client = TestClient(app)  # działa w pamięci, bez Uvicorn

def get_page_content(path: str):
    """Zwraca HTML endpointu jako string."""
    response = client.get(path)
    assert response.status_code == 200
    return response.text

def test_pace_calculation_e2e():
    html_content = get_page_content("/ui")  # pobierz UI

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # zamiast goto serwera, ustawiamy HTML w pamięci
        page.set_content(html_content)

        # wybierz dystans 10km
        page.select_option('select[name="distance_choice"]', "10")
        
        # wpisz czas
        page.fill('input[name="hours"]', "0")
        page.fill('input[name="minutes"]', "50")
        page.fill('input[name="seconds"]', "0")

        # kliknij przycisk
        page.click('text=Calculate Pace')

        # sprawdź wynik
        page.wait_for_selector(".result")
        result_text = page.locator(".result").inner_text()
        assert "Pace" in result_text

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

        page.click('text=Predict')

        page.wait_for_selector(".result")
        result_text = page.locator(".result").inner_text()
        assert "Predicted" in result_text

        browser.close()