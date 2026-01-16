import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.cart_page import CartPage
from core.pages.checkout_page import CheckoutPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
@pytest.mark.xfail(
    reason=(
        "SauceDemo allows checkout flow to proceed with empty cart. "
        "Business rule validation is missing."
    )
)
async def test_checkout_cannot_be_completed_with_empty_cart(page):
    """
    Security / business rule test.

    Expected behavior:
    Checkout must NOT be completable when cart is empty.

    Actual behavior (SauceDemo):
    User can proceed to checkout step two even with empty cart.
    """

    # =========================
    # Login
    # =========================
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        TestData.VALID_USERNAME,
        TestData.VALID_PASSWORD
    )

    # =========================
    # Open cart WITHOUT adding items
    # =========================
    inventory_page = InventoryPage(page)
    await inventory_page.open_cart()

    cart_page = CartPage(page)
    await cart_page.wait_for_cart_page()

    # Safety check
    assert await cart_page.is_empty(), "Cart should be empty before checkout"

    # =========================
    # Go to checkout step one
    # =========================
    await page.goto("https://www.saucedemo.com/checkout-step-one.html")
    assert "/checkout-step-one.html" in page.url

    # =========================
    # Try to continue checkout
    # =========================
    checkout_page = CheckoutPage(page)
    await checkout_page.fill_information(
        first_name="John",
        last_name="Doe",
        postal_code="12345",
    )

    # =========================
    # Assertion (expected to FAIL)
    # =========================
    assert "/checkout-step-two.html" not in page.url, \
        "Checkout must not proceed to step two with empty cart"

