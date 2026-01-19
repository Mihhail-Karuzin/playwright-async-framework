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
@pytest.mark.xfail(
    reason=(
        "Known issue: glitch_user causes significant UI delays. "
        "Inventory page load time exceeds acceptable SLA."
    ),
    strict=False,
)
@allure.severity(allure.severity_level.MINOR)
@allure.feature("Performance")
@allure.story("Glitch user inventory load delay")
async def test_glitch_user_inventory_load_time(page):
    """
    Performance / Quality test (expected defect).

    Expected behavior:
    - Inventory page should load within acceptable SLA.

    Actual behavior (SauceDemo):
    - performance_glitch_user experiences significant delays.

    This test is marked as XFAIL to document the known issue.
    """

    # =========================
    # Load baseline
    # =========================
    baseline = INVENTORY_LOAD_BASELINES["performance_glitch_user"]

    # =========================
    # Login as glitch user
    # =========================
    with allure.step("Login as performance_glitch_user"):
        login_page = LoginPage(page)
        await login_page.open()

        start_time = time.perf_counter()

        await login_page.login(
            TestData.PERFORMANCE_GLITCH_USER,
            TestData.PASSWORD,
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
            name="Inventory load time",
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
            user="performance_glitch_user",
        )

