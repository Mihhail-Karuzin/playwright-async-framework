import time
import pytest
import allure

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.utils.performance import PerformanceChecker
from tests.test_data import TestData
from tests.performance.performance_baselines import INVENTORY_LOAD_BASELINES


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
      within acceptable baseline.

    This test defines the performance baseline
    used for comparison with other user roles
    (e.g. performance_glitch_user).
    """

    # =========================
    # Load baseline
    # =========================
    baseline = INVENTORY_LOAD_BASELINES["standard_user"]

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
    # Validate against baseline
    # =========================
    with allure.step("Validate inventory load time against baseline"):
        checker = PerformanceChecker(
            actual_seconds=load_time,
            baseline_seconds=baseline["expected_seconds"],
            tolerance=baseline["tolerance"],
        )

        assert checker.is_within_threshold(), checker.failure_message(
            metric="Inventory page load",
            user="standard_user",
        )

