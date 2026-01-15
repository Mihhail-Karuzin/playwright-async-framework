import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.cart_page import CartPage
from core.pages.checkout_page import CheckoutPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.feature
async def test_checkout_flow(page):
    """
    Full happy-path checkout flow:
    login → add item → cart → checkout → order complete
    """

    # =========================
    # Login
    # =========================
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        TestData.VALID_USERNAME,
        TestData.VALID_PASSWORD,
    )

    # =========================
    # Add item to cart
    # =========================
    inventory_page = InventoryPage(page)
    await inventory_page.add_item_to_cart_by_name(TestData.ITEM_BACKPACK)
    await inventory_page.open_cart()

    # =========================
    # Cart → Checkout
    # =========================
    cart_page = CartPage(page)
    await cart_page.wait_for_cart_page()
    await cart_page.click_checkout()

    # =========================
    # Checkout flow
    # =========================
    checkout_page = CheckoutPage(page)

    await checkout_page.fill_information(
        first_name="John",
        last_name="Doe",
        postal_code="12345",
    )

    await checkout_page.finish_checkout()

    # =========================
    # Assert success
    # =========================
    assert await checkout_page.is_order_complete(), "Order should be completed successfully"

