# config/settings.py
class Settings:
    BASE_URL = "https://playwright.dev"
    BROWSER = "chromium"      # Можно "chromium", "firefox" или "webkit"
    HEADLESS = False          # False — видимый браузер, True — без интерфейса
    WINDOW_SIZE = {"width": 1280, "height": 720}
    DEFAULT_TIMEOUT = 5000
