from playwright.sync_api import sync_playwright
import threading
import uvicorn
import time  # do drobnego opóźnienia

# Funkcja uruchamiająca serwer FastAPI w tle
def run_server():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)

def test_pace_calculation_e2e():
    # Uruchom serwer w tle
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Poczekaj chwilę, żeby serwer zdążył wystartować
    time.sleep(1)  

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://127.0.0.1:8000/ui")  # teraz serwer działa

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
    # Uruchom serwer w tle
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # poczekaj aż serwer startuje

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://127.0.0.1:8000/ui")

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
        