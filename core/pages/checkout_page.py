from core.pages.checkout_step_one_page import CheckoutStepOnePage
from core.pages.checkout_step_two_page import CheckoutStepTwoPage
from core.pages.checkout_complete_page import CheckoutCompletePage


class CheckoutPage:
    def __init__(self, page):
        self.step_one = CheckoutStepOnePage(page)
        self.step_two = CheckoutStepTwoPage(page)
        self.complete = CheckoutCompletePage(page)

    async def fill_information(self, first_name: str, last_name: str, postal_code: str):
        await self.step_one.fill_information(
            first_name=first_name,
            last_name=last_name,
            postal_code=postal_code,
        )

    async def finish_checkout(self):
        await self.step_two.finish_checkout()

    async def is_order_complete(self) -> bool:
        return await self.complete.is_order_complete()

    async def get_step_one_error_text(self) -> str:
        return await self.step_one.get_error_text()

