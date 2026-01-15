import pytest
from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.cart_page import CartPage
from config.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.feature
async def test_add_item_to_cart(page):
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        TestData.VALID_USERNAME,
        TestData.VALID_PASSWORD
    )

    inventory_page = InventoryPage(page)
    await inventory_page.add_item_to_cart_by_name(TestData.ITEM_BACKPACK)
    await inventory_page.open_cart()

    cart_page = CartPage(page)
    count = await cart_page.get_items_count()

    assert count == 1, "Item was not added to the cart"

