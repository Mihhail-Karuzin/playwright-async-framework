import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.cart_page import CartPage
from config.settings import Settings


@pytest.mark.asyncio
@pytest.mark.feature
async def test_cart_contains_correct_items(page):
    items = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
    ]

    # Login
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        Settings.VALID_USERNAME,
        Settings.VALID_PASSWORD,
    )

    # Add items
    inventory_page = InventoryPage(page)
    for item in items:
        await inventory_page.add_item_to_cart_by_name(item)

    await inventory_page.open_cart()

    # Verify cart
    cart_page = CartPage(page)
    cart_items = await cart_page.get_items_names()

    assert sorted(cart_items) == sorted(items)
