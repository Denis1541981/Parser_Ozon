
from pathlib import Path

# Paths

OUTPUT_PATH = Path.home() / "Desktop" / "Sort values.xlsx"

#BASE URL
BASE_URL='https://www.ozon.ru'


# Browser
HEADLESS = False
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
LOCALE = "ru-RU"
TIMEZONE = "Asia/Novosibirsk"

# Delays (seconds)
SCROLL_DELAY_MIN = 0.3
SCROLL_DELAY_MAX = 1.5
NAVIGATION_TIMEOUT = 15000
ACTION_DELAY_MIN = 0.5
ACTION_DELAY_MAX = 2.0

# Limits
MAX_PRODUCTS_TO_PARSE = 50
SCROLL_COUNT = 30