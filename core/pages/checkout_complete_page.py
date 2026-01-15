from playwright.async_api import Page, Locator
from core.base_page import BasePage
from core.utils.logger import get_logger

logger = get_logger("CheckoutCompletePage")


class CheckoutCompletePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.complete_container: Locator = page.locator(
            ".checkout_complete_container"
        )
        self.complete_header: Locator = page.locator(
            ".complete-header"
        )

    async def is_order_complete(self) -> bool:
        logger.info("Checking if order is completed successfully")

        await self.wait_for_url("/checkout-complete.html")

        return (
            await self.complete_container.is_visible()
            and await self.complete_header.is_visible()
        )
