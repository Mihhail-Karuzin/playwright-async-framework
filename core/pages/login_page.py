import re
from playwright.async_api import expect
from config.settings import Settings
from core.utils.logger import get_logger

logger = get_logger("LoginPage")


class LoginPage:
    def __init__(self, page):
        self.page = page

        # =========================
        # Locators
        # =========================
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    # =========================
    # Navigation
    # =========================
    async def open(self):
        logger.info(f"Navigating to URL: {Settings.BASE_URL}")
        await self.page.goto(Settings.BASE_URL)

        await expect(self.page).to_have_url(
            re.compile(r"https://www\.saucedemo\.com/?"),
            timeout=Settings.TIMEOUT_MEDIUM,
        )

    # =========================
    # Actions
    # =========================
    async def login(self, username: str, password: str):
        logger.info(f"Logging in as user: '{username}'")

        await self.username_input.fill(username)
        await self.password_input.fill(password)
        await self.login_button.click()

    # =========================
    # State / Assertions helpers
    # =========================
    async def is_error_visible(self) -> bool:
        return await self.error_message.is_visible()

    async def get_error_text(self) -> str:
        """
        Returns error message text.
        Used for strict content assertions.
        """
        await self.error_message.wait_for(
            state="visible",
            timeout=Settings.TIMEOUT_SHORT,
        )
        return (await self.error_message.text_content()).strip()

    async def is_logged_in(self) -> bool:
        """
        User is considered logged in
        when inventory page is opened.
        """
        return "/inventory.html" in self.page.url


