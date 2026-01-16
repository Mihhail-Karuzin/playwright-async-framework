import pytest
import allure

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
    ),
    strict=False,  # Важно: тест будет XFAIL, а не будет валить сборку
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Checkout")
@allure.story("Prevent checkout with empty cart")
async def test_checkout_cannot_be_completed_with_empty_cart(page):
    """
    Security / Business rule test (expected defect):
    Checkout must not be completable when cart is empty.

    Current SauceDemo behavior:
    - Allows user to open checkout-step-one and continue to step-two even with empty cart.
    That is a business rule gap, so we mark test as XFAIL (known issue).
    """

    # =========================
    # Login
    # =========================
    with allure.step("Login as valid user"):
        login_page = LoginPage(page)
        await login_page.open()
        await login_page.login(
            TestData.VALID_USERNAME,
            TestData.VALID_PASSWORD
        )

    # =========================
    # Open cart WITHOUT adding items
    # =========================
    with allure.step("Open cart without adding items"):
        inventory_page = InventoryPage(page)
        await inventory_page.open_cart()

        cart_page = CartPage(page)
        await cart_page.wait_for_cart_page()

        # sanity check: cart действительно пустой
        assert await cart_page.is_empty(), "Cart should be empty before checkout attempt"

    # =========================
    # Try checkout with empty cart
    # =========================
    with allure.step("Try to access checkout step one directly"):
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        assert "/checkout-step-one.html" in page.url, "Checkout step one should open"

    with allure.step("Fill checkout information and try to continue"):
        checkout_page = CheckoutPage(page)
        await checkout_page.fill_information(
            first_name="John",
            last_name="Doe",
            postal_code="12345",
        )

    # =========================
    # Assert (expected business rule)
    # =========================
    with allure.step("Verify checkout does NOT proceed to step two with empty cart"):
        # ИДЕАЛЬНОЕ поведение для магазина:
        # если корзина пустая — нельзя переходить на step-two
        assert "/checkout-step-two.html" not in page.url, (
            "Checkout must NOT proceed to step two when cart is empty. "
            "This is a business rule / security gap."
        )


