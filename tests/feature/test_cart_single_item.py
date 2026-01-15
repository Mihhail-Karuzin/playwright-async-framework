import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from config.settings import Settings


@pytest.mark.asyncio
@pytest.mark.feature
async def test_cart_add_single_item(page):
    """
    Add one item to cart and verify:
    - cart badge = 1
    - item marked as added (Remove button visible)
    """

    # ===== Login =====
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        Settings.VALID_USERNAME,
        Settings.VALID_PASSWORD
    )

    # ===== Inventory =====
    inventory_page = InventoryPage(page)

    item_name = "Sauce Labs Backpack"

    await inventory_page.add_item_to_cart_by_name(item_name)

    # ===== Assertions =====
    cart_count = await inventory_page.get_cart_badge_count()
    assert cart_count == 1, "Cart badge should show 1 item"

    assert await inventory_page.is_item_added(item_name), (
        f"Item '{item_name}' should be marked as added"
    )
