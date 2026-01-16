import time
import pytest
import allure

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
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
    - Inventory page should load within acceptable SLA (<= 3 seconds).

    Actual behavior (SauceDemo):
    - glitch_user experiences significant delays.
    """

    SLA_SECONDS = 3.0

    # =========================
    # Login as glitch_user
    # =========================
    with allure.step("Login as glitch_user"):
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
    # Assert SLA
    # =========================
    with allure.step("Verify inventory load time meets SLA"):
        assert load_time <= SLA_SECONDS, (
            f"Inventory page loaded in {load_time:.2f}s, "
            f"which exceeds SLA of {SLA_SECONDS:.1f}s"
        )
