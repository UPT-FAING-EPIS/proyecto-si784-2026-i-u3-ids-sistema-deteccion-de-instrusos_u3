import os
import threading
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from playwright.sync_api import expect, sync_playwright
from werkzeug.serving import make_server

from src.storage import AlertStorage
from web import app as dashboard_app


def save_screenshot(page, name):
    screenshot_dir = os.environ.get("UI_SCREENSHOT_DIR")
    if not screenshot_dir:
        return
    Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(Path(screenshot_dir) / name), full_page=True)


def new_context(browser):
    video_dir = os.environ.get("UI_VIDEO_DIR")
    if not video_dir:
        return browser.new_context()
    Path(video_dir).mkdir(parents=True, exist_ok=True)
    return browser.new_context(
        record_video_dir=video_dir,
        record_video_size={"width": 1280, "height": 720},
    )


def save_video(page, name):
    video_dir = os.environ.get("UI_VIDEO_DIR")
    if not video_dir or page.video is None:
        return
    source = Path(page.video.path())
    target = Path(video_dir) / name
    if source.exists():
        source.replace(target)


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
        context = new_context(browser)
        page = context.new_page()

        page.goto(live_dashboard, wait_until="networkidle")

        expect(page.locator("h1")).to_contain_text("TrafficWatch IDS")
        expect(page.locator("#dashboardNav")).to_contain_text("Dashboard")
        expect(page.locator("#statusNav")).to_contain_text("Estado IDS")
        expect(page.locator("#historyNav")).to_contain_text("Historial")
        expect(page.locator("#rulesNav")).to_contain_text("Reglas IDS")
        save_screenshot(page, "dashboard-home.png")

        page.close()
        context.close()
        save_video(page, "trafficwatch-dashboard-home.webm")
        browser.close()


@pytest.mark.ui
def test_attack_lab_renders_remote_lab_buttons(live_dashboard):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = new_context(browser)
        page = context.new_page()

        page.goto(f"{live_dashboard}/attack-lab", wait_until="networkidle")

        expect(page.locator("h1")).to_contain_text("TrafficWatch Lab")
        expect(page.get_by_role("button", name="Escanear IP")).to_be_visible()
        expect(page.get_by_role("button", name="Enviar").first).to_be_visible()
        save_screenshot(page, "attack-lab.png")

        page.close()
        context.close()
        save_video(page, "trafficwatch-attack-lab.webm")
        browser.close()
