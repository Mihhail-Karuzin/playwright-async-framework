from playwright.async_api import Page, Locator
from core.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_items: Locator = page.locator(".cart_item")
        self.cart_item_names: Locator = page.locator(".inventory_item_name")
        self.remove_buttons: Locator = page.locator("button[data-test^='remove']")

        self.checkout_button: Locator = page.locator("[data-test='checkout']")
        self.continue_shopping_button: Locator = page.locator(
            "[data-test='continue-shopping']"
        )

    async def wait_for_cart_page(self):
        await self.wait_for_url("/cart.html")
        if await self.cart_items.count() > 0:
            await self.wait_for_locator(self.cart_items.first)

    async def get_items_count(self) -> int:
        await self.wait_for_cart_page()
        return await self.cart_items.count()

    async def get_items_names(self) -> list[str]:
        await self.wait_for_cart_page()
        return await self.cart_item_names.all_inner_texts()

    async def remove_item_by_name(self, item_name: str):
        button = self.page.locator(
            f"//div[text()='{item_name}']/ancestor::div[@class='cart_item']//button"
        )
        await self.click(button)

    async def remove_all_items(self):
        await self.wait_for_cart_page()
        while await self.remove_buttons.count() > 0:
            await self.remove_buttons.nth(0).click()

    async def is_empty(self) -> bool:
        await self.wait_for_cart_page()
        return await self.cart_items.count() == 0

    async def click_checkout(self):
        await self.wait_for_cart_page()
        await self.click(self.checkout_button)

