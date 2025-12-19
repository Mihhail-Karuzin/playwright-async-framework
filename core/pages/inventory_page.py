from playwright.async_api import Page, Locator
from core.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_items: Locator = page.locator(".inventory_item")
        self.cart_link: Locator = page.locator(".shopping_cart_link")

    def add_to_cart_button(self, item_name: str) -> Locator:
        return self.page.locator(
            f'//div[text()="{item_name}"]/ancestor::div[@class="inventory_item"]//button'
        )

    async def wait_for_inventory_page(self):
        await self.wait_for_url("/inventory.html")
        await self.wait_for_locator(self.inventory_items.first)

    async def add_item_to_cart_by_name(self, item_name: str):
        await self.wait_for_inventory_page()
        await self.click(self.add_to_cart_button(item_name))

    async def open_cart(self):
        await self.click(self.cart_link)

    async def get_items_count(self) -> int:
        await self.wait_for_inventory_page()
        return await self.inventory_items.count()


