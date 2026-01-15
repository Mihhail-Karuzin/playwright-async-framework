# # config/settings.py
#
# class Settings:
#     # Base URL of the application under test
#     BASE_URL: str = "https://www.saucedemo.com"
#
#     # Default browser settings
#     HEADLESS: bool = False           # whether to run browser in headless mode
#     WINDOW_SIZE: tuple | None = None # e.g. (1920, 1080) or None to use default
#
#     # Timeouts (in milliseconds) or other global timeouts
#     TIMEOUT: int = 30000             # 30 seconds as default timeout for page operations
#
#     # (Add more global settings if needed)
#
#
# #config/settings.py

class Settings:
    # ---- Base URL
    BASE_URL = "https://www.saucedemo.com"

    # ---- Timeouts (milliseconds)
    TIMEOUT_SHORT = 2_000
    TIMEOUT_MEDIUM = 5_000
    TIMEOUT_LONG = 10_000

    # ⬇️ REQUIRED
    # Used in BasePage.wait_for_url()
    TIMEOUT = TIMEOUT_MEDIUM

    # ---- Playwright
    HEADLESS = True

    # ---- Test data
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"


