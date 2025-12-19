from playwright.async_api import Page, Locator
from core.base_page import BasePage
from config.settings import Settings


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = page.get_by_placeholder("Username")
        self.password_input: Locator = page.get_by_placeholder("Password")
        self.login_button: Locator = page.locator('[data-test="login-button"]')
        self.error_message: Locator = page.locator('[data-test="error"]')

    async def open(self):
        await self.goto(Settings.BASE_URL)

    async def login(self, username: str, password: str):
        await self.fill(self.username_input, username)
        await self.fill(self.password_input, password)
        await self.click(self.login_button)

    async def is_error_visible(self) -> bool:
        return await self.is_visible(self.error_message)

    async def is_logged_in(self) -> bool:
        return await self.page.locator(".inventory_container").is_visible()

