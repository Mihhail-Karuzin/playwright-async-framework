import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.cart_page import CartPage
from core.pages.checkout_page import CheckoutPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
@pytest.mark.xfail(
    reason="Known issue: checkout can be completed even when cart is empty",
    strict=False,
)
async def test_checkout_finish_without_items(page):
    """
    Security / business rule test.

    Expected behavior:
    - Checkout MUST NOT be completed if cart is empty.

    Actual behavior (SauceDemo):
    - User can finish checkout with empty cart.

    This test documents the vulnerability.
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
    # Open cart WITHOUT items
    # =========================
    inventory_page = InventoryPage(page)
    await inventory_page.open_cart()

    cart_page = CartPage(page)
    await cart_page.wait_for_cart_page()
    assert await cart_page.is_empty(), "Cart must be empty before checkout"

    # =========================
    # Go directly to checkout step two
    # (bypassing step one)
    # =========================
    await page.goto("https://www.saucedemo.com/checkout-step-two.html")

    checkout_page = CheckoutPage(page)

    # =========================
    # Try to finish checkout
    # =========================
    await checkout_page.finish_checkout()

    # =========================
    # ASSERT (expected secure behavior)
    # =========================
    assert "/checkout-complete.html" not in page.url, (
        "Checkout must not be completed with empty cart"
    )
