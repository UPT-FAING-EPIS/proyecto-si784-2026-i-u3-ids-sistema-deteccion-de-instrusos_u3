import threading
from tempfile import TemporaryDirectory

import pytest
from playwright.sync_api import expect, sync_playwright
from werkzeug.serving import make_server

from src.storage import AlertStorage
from web import app as dashboard_app


@pytest.fixture(scope="session")
def live_dashboard():
    temp_dir = TemporaryDirectory()
    temp_path = temp_dir.name

    dashboard_app.storage = AlertStorage(f"{temp_path}/alerts.json")
    dashboard_app.traffic_storage = AlertStorage(f"{temp_path}/traffic.json", max_records=20)
    dashboard_app.policy_storage = AlertStorage(f"{temp_path}/policies.json")
    dashboard_app.STATUS_FILE = f"{temp_path}/status.json"

    server = make_server("127.0.0.1", 0, dashboard_app.app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{server.server_port}"

    server.shutdown()
    thread.join(timeout=5)
    temp_dir.cleanup()


@pytest.mark.ui
def test_dashboard_home_renders_main_navigation(live_dashboard):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto(live_dashboard, wait_until="networkidle")

        expect(page.locator("h1")).to_contain_text("TrafficWatch IDS")
        expect(page.locator("#dashboardNav")).to_contain_text("Dashboard")
        expect(page.locator("#statusNav")).to_contain_text("Estado IDS")
        expect(page.locator("#historyNav")).to_contain_text("Historial")
        expect(page.locator("#rulesNav")).to_contain_text("Reglas IDS")

        browser.close()


@pytest.mark.ui
def test_attack_lab_renders_remote_lab_buttons(live_dashboard):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.goto(f"{live_dashboard}/attack-lab", wait_until="networkidle")

        expect(page.locator("h1")).to_contain_text("TrafficWatch Lab")
        expect(page.locator("button").first).to_contain_text("Enviar")

        browser.close()
