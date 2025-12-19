# tests/feature/test_inventory.py

import pytest
from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from config.test_data import TestData

@pytest.mark.asyncio
async def test_inventory_items_present_after_login(page):
    """
    Test that inventory items are displayed after successful login.
    """
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)

    inventory_page = InventoryPage(page)
    count = await inventory_page.get_items_count()
    assert count > 0, f"Expected at least 1 item, but found {count}"
