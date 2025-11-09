#!usr/bin/python


import time
import random
import re
from typing import Set, List, Dict
from config.selectors import SELECTORS
from config.settings import *
from utils.logger import Logger
from utils.helpers import safe_inner_text, safe_attr



logger = Logger(__name__)

class OzonParser:
    def __init__(self, query: str):
        self.query = query
        self.context = None
        self.search_page = None
        self.detail_page = None


    def setup_pages(self, context):
        self.context = context
        self.search_page = context.new_page()
        self.search_page.set_default_timeout(NAVIGATION_TIMEOUT)
        self.detail_page = context.new_page()


    def random_delay(self, min_s: float = None, max_s: float = None):
        min_s = min_s or ACTION_DELAY_MIN
        max_s = max_s or ACTION_DELAY_MAX
        time.sleep(random.uniform(min_s, max_s))


    def scroll_down(self, page, scrolls=SCROLL_COUNT):
        logger.info("Начинаю прокрутку страницы...")
        for i in range(scrolls):
            try:
                page.mouse.wheel(0, 300)
                self.random_delay(SCROLL_DELAY_MIN, SCROLL_DELAY_MAX)
            except Exception as e:
                logger.warning(f"Прокрутка {i}: {e}")
        logger.info("Прокрутка завершена.")


    def search_products(self, page):
        page.goto(BASE_URL, wait_until="domcontentloaded")
        self.random_delay(1, 2)

        input_el = page.locator(SELECTORS["search_input"])
        input_el.scroll_into_view_if_needed()
        input_el.click()
        self.random_delay(0.3, 0.8)
        input_el.type(self.query, delay=0.08)
        self.random_delay(0.5, 1.2)

        page.locator(SELECTORS["search_button"]).click()
        page.wait_for_selector(SELECTORS["search_results_container"], timeout=10000)


    def collect_urls(self, page) -> Set[str]:
        self.scroll_down(page)
        links = page.locator(SELECTORS["product_link"]).all()
        urls = set()
        for link in links[:MAX_PRODUCTS_TO_PARSE]:
            href = link.get_attribute("href")
            if href and "/product/" in href:
                full_url = BASE_URL + href.split("?")[0]  # убираем utm & params
                urls.add(full_url)
        logger.info(f"Собрано {len(urls)} URL")
        return urls


    def parse_product(self, page, url: str) -> Dict | None:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT)
            page.wait_for_selector(SELECTORS["title"], timeout=5000)

            title = safe_inner_text(page, SELECTORS["title"])
            sku_text = safe_inner_text(page, SELECTORS["sku_button"])
            article = "".join(re.findall(r"\d+", sku_text or "")) or "N/A"

            price_card_text = safe_inner_text(page, SELECTORS["price_card"])
            price_card = int("".join(re.findall(r"\d+", price_card_text or ""))) if price_card_text else None

            price_regular_text = safe_inner_text(page, SELECTORS["price_regular"])
            price_regular = int("".join(re.findall(r"\d+", price_regular_text or ""))) if price_regular_text else None

            rating_block_text = safe_inner_text(page, SELECTORS["rating_block"])
            rating = reviews = "N/A"
            if rating_block_text and " • " in rating_block_text:
                parts = rating_block_text.split(" • ")
                rating = float(parts[0].strip())
                reviews = int(parts[1].split(" ")[0].strip())

            reviews_url = safe_attr(page, SELECTORS["reviews_link"], "href")
            clean_reviews_url = BASE_URL + (reviews_url or "").replace("/reviews/", "") if reviews_url else url

            return {
                "article": article,
                "title": title,
                "price_in_card": price_card,
                "price_not_in_card": price_regular,
                "reciting": rating,
                "number of reviews": reviews,
                "url": clean_reviews_url,
            }

        except Exception as e:
            logger.error(f"Ошибка парсинга {url}: {e}")
            return None

    def scrape_products(self, page, urls: Set[str]) -> List[Dict]:
        products = []
        for i, url in enumerate(urls, 1):
            logger.info(f"[{i}/{len(urls)}] Парсинг: {url}")
            data = self.parse_product(page, url)
            if data:
                products.append(data)
            self.random_delay(1.5, 3.0)  # уважаем сервер
        logger.info(f"Успешно спарсено: {len(products)} из {len(urls)}")
        return products