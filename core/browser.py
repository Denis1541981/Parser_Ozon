
from contextlib import contextmanager
from playwright.sync_api import sync_playwright
from config.settings import *

@contextmanager
def create_context(headless: bool = False):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless, args=[
        "--disable-blink-features=AutomationControlled",
        "--disable-features=IsolateOrigins,site-per-process"
    ])
    context = browser.new_context(
        viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        user_agent=USER_AGENT,
        java_script_enabled=True,
        permissions=["geolocation"],
    )
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    """)
    try:
        yield context
    finally:
        context.close()
        browser.close()
        p.stop()