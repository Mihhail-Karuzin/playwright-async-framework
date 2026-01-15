from playwright.async_api import Page, Locator
from core.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.finish_button: Locator = page.locator("#finish")

    async def wait_for_page(self):
        await self.wait_for_url("/checkout-step-two.html")

    async def finish_checkout(self):
        await self.wait_for_page()
        await self.click(self.finish_button)
