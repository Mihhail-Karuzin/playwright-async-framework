import time
import pytest
import allure

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.performance
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Performance")
@allure.story("Standard user inventory load baseline")
async def test_standard_user_inventory_load_time(page):
    """
    Performance baseline test.

    Expected behavior:
    - Inventory page for standard_user must load
      within acceptable SLA (<= 3 seconds).

    This test serves as a baseline to compare against
    performance_glitch_user behavior.
    """

    SLA_SECONDS = 3.0

    # =========================
    # Login as standard_user
    # =========================
    with allure.step("Login as standard_user"):
        login_page = LoginPage(page)
        await login_page.open()

        start_time = time.perf_counter()

        await login_page.login(
            TestData.VALID_USERNAME,
            TestData.VALID_PASSWORD,
        )

    # =========================
    # Wait for inventory page
    # =========================
    with allure.step("Wait for inventory page to load"):
        inventory_page = InventoryPage(page)
        await inventory_page.wait_for_inventory_page()

        end_time = time.perf_counter()
        load_time = end_time - start_time

        allure.attach(
            f"{load_time:.2f} seconds",
            name="Inventory load time (standard_user)",
            attachment_type=allure.attachment_type.TEXT,
        )

    # =========================
    # Assert SLA
    # =========================
    with allure.step("Verify inventory load time meets SLA"):
        assert load_time <= SLA_SECONDS, (
            f"Inventory page loaded in {load_time:.2f}s, "
            f"which exceeds SLA of {SLA_SECONDS:.1f}s"
        )
