import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from config.settings import Settings


@pytest.mark.asyncio
@pytest.mark.feature
@pytest.mark.parametrize(
    "items",
    [
        ["Sauce Labs Backpack"],
        ["Sauce Labs Backpack", "Sauce Labs Bike Light"],
        [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
        ],
    ],
)
async def test_add_multiple_items_to_cart(page, items):
    """
    Feature test:
    - login
    - add N items to cart
    - verify cart badge count
    """

    # 🔐 Login
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        Settings.VALID_USERNAME,
        Settings.VALID_PASSWORD,
    )

    # 🛒 Inventory actions
    inventory_page = InventoryPage(page)

    for item in items:
        await inventory_page.add_item_to_cart_by_name(item)

    # 🔢 Assert cart badge count
    cart_badge = page.locator(".shopping_cart_badge")
    await cart_badge.wait_for(state="visible")

    badge_text = await cart_badge.inner_text()
    assert int(badge_text) == len(items)
