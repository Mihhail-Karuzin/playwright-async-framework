# core/pages/header_page.py

from core.base_page import BasePage
from playwright.async_api import Page, Locator

class HeaderPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.burger_menu_button: Locator = page.locator("#react-burger-menu-btn")
        self.logout_link: Locator = page.locator("#logout_sidebar_link")

    async def open_menu(self):
        await self.burger_menu_button.click()

    async def logout(self):
        await self.open_menu()
        await self.logout_link.click()
