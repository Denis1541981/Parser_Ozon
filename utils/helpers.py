
from playwright.sync_api import Page

def safe_inner_text(page: Page, selector: str, default: str = "") -> str:
    try:
        return page.locator(selector).inner_text().strip()
    except Exception:
        return default

def safe_attr(page: Page, selector: str, attr: str, default: str = "") -> str:
    try:
        return page.locator(selector).get_attribute(attr) or default
    except Exception:
        return default