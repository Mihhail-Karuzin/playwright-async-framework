import pytest
import allure

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.header_page import HeaderPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
@pytest.mark.xfail(
    reason=(
        "SauceDemo does not invalidate session cookies on logout. "
        "Old cookies can restore access to protected pages. "
        "This is a known security limitation of the demo application."
    ),
    strict=False,
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Session Management")
@allure.story("Reuse cookies after logout")
async def test_reuse_cookies_after_logout_does_not_restore_access(context, page):
    """
    Security test (expected defect):

    Logout must invalidate session cookies.
    Reusing old cookies must NOT restore access.

    Actual SauceDemo behavior:
    - Old cookies remain valid after logout
    - Protected pages are accessible again
    """

    # =========================
    # Login
    # =========================
    with allure.step("Login as valid user"):
        login_page = LoginPage(page)
        await login_page.open()
        await login_page.login(
            TestData.VALID_USERNAME,
            TestData.VALID_PASSWORD
        )

        inventory_page = InventoryPage(page)
        await inventory_page.wait_for_inventory_page()

    # =========================
    # Save cookies
    # =========================
    with allure.step("Save authentication cookies"):
        saved_cookies = await context.cookies()

    # =========================
    # Logout
    # =========================
    with allure.step("Logout from application"):
        header = HeaderPage(page)
        await header.logout()

    # =========================
    # Reuse cookies in new context
    # =========================
    with allure.step("Reuse cookies in new browser context"):
        new_context = await context.browser.new_context()
        try:
            await new_context.add_cookies(saved_cookies)
            new_page = await new_context.new_page()

            await new_page.goto("https://www.saucedemo.com/inventory.html")

            # Expected secure behavior:
            assert (
                new_page.url.endswith("/")
                or "login" in new_page.url
            ), (
                "Access restored by old cookies. "
                "Session invalidation on logout is missing."
            )

        finally:
            await new_context.close()
