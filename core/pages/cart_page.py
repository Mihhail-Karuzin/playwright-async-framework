from playwright.async_api import Page, Locator
from core.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items: Locator = page.locator(".cart_item")

    async def get_cart_items_count(self) -> int:
        await self.wait_for_locator(self.cart_items.first)
        return await self.cart_items.count()

