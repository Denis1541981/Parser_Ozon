SELECTORS = {
    # Поиск
    "search_input": "input[placeholder*='Искать на Ozon'], input[placeholder*='Search on Ozon']",
    "search_button": "button[type='submit']",
    "search_results_container": "a[href*='/product/']",

    # Сбор ссылок
    "product_link": "a[href*='/product/']",

    # Карточка товара
    "title": "[data-widget='webProductHeading'] h1, h1[data-partner='productTitle']",
    "sku_button": "button[data-widget='webDetailSKU']",
    "price_card": "span.tsHeadline600Large, .tsHeadline600Large",
    "price_regular": "span.pdp_b7f.tsHeadline500Medium, .pdp_b7f .tsHeadline500Medium",
    "rating_block": "div[data-widget='webSingleProductScore']",
    "rating_text": "div.ga5_3_10-a2.tsBodyControl500Medium",
    "reviews_link": "a[href*='/reviews/']",
}
