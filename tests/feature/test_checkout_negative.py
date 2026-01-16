import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.cart_page import CartPage
from core.pages.checkout_page import CheckoutPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.feature
@pytest.mark.regression
@pytest.mark.parametrize(
    "first_name,last_name,postal_code,expected_error",
    [
        ("", "Doe", "12345", "Error: First Name is required"),
        ("John", "", "12345", "Error: Last Name is required"),
        ("John", "Doe", "", "Error: Postal Code is required"),
        ("", "", "", "Error: First Name is required"),
    ],
)
async def test_checkout_missing_required_fields(
    page,
    first_name,
    last_name,
    postal_code,
    expected_error,
):
    """
    Negative checkout tests:
    missing first name / last name / postal code
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
    # Add item → cart
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
    # Checkout step one
    # =========================
    checkout_page = CheckoutPage(page)

    await checkout_page.fill_information(
        first_name=first_name,
        last_name=last_name,
        postal_code=postal_code,
    )

    # =========================
    # Assert error
    # =========================
    error_text = await checkout_page.get_step_one_error_text()
    assert error_text == expected_error
