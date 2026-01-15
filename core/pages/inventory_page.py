from playwright.async_api import Page, Locator
from core.base_page import BasePage
from config.settings import Settings
from core.utils.logger import get_logger

logger = get_logger("InventoryPage")


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.inventory_items: Locator = page.locator(".inventory_item")
        self.cart_link: Locator = page.locator(".shopping_cart_link")
        self.cart_badge: Locator = page.locator(".shopping_cart_badge")

    # =====================================================
    # Dynamic locators
    # =====================================================
    def add_to_cart_button(self, item_name: str) -> Locator:
        return self.page.locator(
            f'//div[text()="{item_name}"]'
            f'/ancestor::div[@class="inventory_item"]//button'
        )

    def remove_from_cart_button(self, item_name: str) -> Locator:
        return self.page.locator(
            f'//div[text()="{item_name}"]'
            f'/ancestor::div[@class="inventory_item"]//button[text()="Remove"]'
        )

    # =====================================================
    # Page state
    # =====================================================
    async def wait_for_inventory_page(self):
        logger.info("Waiting for inventory page")
        await self.wait_for_url("/inventory.html")
        await self.wait_for_locator(self.inventory_items.first)

    # =====================================================
    # Actions
    # =====================================================
    async def add_item_to_cart_by_name(self, item_name: str):
        logger.info(f"Adding item to cart: {item_name}")
        await self.wait_for_inventory_page()
        await self.click(self.add_to_cart_button(item_name))

    async def remove_item_from_cart_by_name(self, item_name: str):
        logger.info(f"Removing item from cart: {item_name}")
        await self.wait_for_inventory_page()
        await self.click(self.remove_from_cart_button(item_name))

    async def open_cart(self):
        logger.info("Opening cart")
        await self.click(self.cart_link)

    # =====================================================
    # Assertions helpers (NO asserts inside!)
    # =====================================================
    async def get_items_count(self) -> int:
        await self.wait_for_inventory_page()
        return await self.inventory_items.count()

    async def get_cart_badge_count(self) -> int:
        if await self.cart_badge.is_visible():
            return int(await self.cart_badge.text_content())
        return 0

    async def is_item_added(self, item_name: str) -> bool:
        return await self.remove_from_cart_button(item_name).is_visible()

    async def is_item_removed(self, item_name: str) -> bool:
        return await self.add_to_cart_button(item_name).is_visible()
