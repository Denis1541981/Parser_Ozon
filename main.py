#!usr/bin/python

import sys
from config.settings import OUTPUT_PATH
from core.browser import create_context
from core.parser import OzonParser
from utils.logger import Logger
import pandas as pd


logger = Logger(__name__)

def save_to_excel(data: list, path):
    if not data:
        logger.warning("Нет данных для сохранения")
        return

    df = pd.DataFrame(data)
    if "article" in df.columns:
        df.set_index("article", inplace=True)

    df_sorted = df.sort_values(by="reciting", ascending=False, key=lambda x: pd.to_numeric(x.str.replace(',', '.'), errors='coerce'))

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="raw")
        df_sorted.to_excel(writer, sheet_name="raw", startrow=len(df) + 3)
    logger.info(f"✅ Данные сохранены: {path}")


def main():
    query = input("🔍 Введите запрос: ").strip() #or sys.argv[1] if len(sys.argv) > 1 else None
    if not query:
        logger.error("Запрос обязателен")
        return

    logger.info(f"▶️ Парсинг: {query}")

    with create_context(headless=False) as context:
        page = context.new_page()
        parser = OzonParser(query)

        try:
            parser.search_products(page)   # ← page как аргумент
            urls = parser.collect_urls(page)
            products = parser.scrape_products(page, urls)  # ← page + urls
            if products:
                save_to_excel(products, OUTPUT_PATH)
            else:
                logger.warning("Нет данных")

        except Exception as e:
            logger.error("Критическая ошибка")
            page.screenshot(path="error.png")
            raise



if __name__ == "__main__":
    main()





