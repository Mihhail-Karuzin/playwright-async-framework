from playwright.async_api import Page, Locator
from core.base_page import BasePage
from core.utils.logger import get_logger

logger = get_logger("CheckoutStepOnePage")


class CheckoutStepOnePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.first_name_input: Locator = page.locator("#first-name")
        self.last_name_input: Locator = page.locator("#last-name")
        self.postal_code_input: Locator = page.locator("#postal-code")
        self.continue_button: Locator = page.locator("#continue")

    async def fill_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ):
        logger.info("Filling checkout step one information")

        await self.wait_for_url("/checkout-step-one.html")

        await self.first_name_input.fill(first_name)
        await self.last_name_input.fill(last_name)
        await self.postal_code_input.fill(postal_code)

        await self.click(self.continue_button)

