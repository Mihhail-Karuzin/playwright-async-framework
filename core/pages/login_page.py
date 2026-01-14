# from playwright.async_api import Page, Locator
# from core.base_page import BasePage
# from config.settings import Settings
#
#
# class LoginPage(BasePage):
#     def __init__(self, page: Page):
#         super().__init__(page)
#         self.username_input: Locator = page.get_by_placeholder("Username")
#         self.password_input: Locator = page.get_by_placeholder("Password")
#         self.login_button: Locator = page.locator('[data-test="login-button"]')
#         self.error_message: Locator = page.locator('[data-test="error"]')
#
#     async def open(self):
#         await self.goto(Settings.BASE_URL)
#
#     async def login(self, username: str, password: str):
#         await self.fill(self.username_input, username)
#         await self.fill(self.password_input, password)
#         await self.click(self.login_button)
#
#     async def is_error_visible(self) -> bool:
#         return await self.is_visible(self.error_message)
#
#     async def is_logged_in(self) -> bool:
#         return await self.page.locator(".inventory_container").is_visible()



import re
from playwright.async_api import expect
from config.settings import Settings
from core.utils.logger import get_logger

logger = get_logger("LoginPage")


class LoginPage:
    def __init__(self, page):
        self.page = page

        # locators
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    async def open(self):
        logger.info(f"Navigating to URL: {Settings.BASE_URL}")
        await self.page.goto(Settings.BASE_URL)

        await expect(self.page).to_have_url(
            re.compile(r"https://www\.saucedemo\.com/?"),
            timeout=Settings.TIMEOUT_MEDIUM,
        )

    async def login(self, username: str, password: str):
        logger.info(f"Logging in as user: '{username}'")

        await self.username_input.fill(username)
        await self.password_input.fill(password)
        await self.login_button.click()

    async def is_error_visible(self) -> bool:
        return await self.error_message.is_visible()

    async def is_logged_in(self) -> bool:
        return "/inventory.html" in self.page.url

