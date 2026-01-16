import pytest
import allure

from core.pages.login_page import LoginPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Authentication")
@allure.story("Locked out user access")
async def test_locked_out_user_cannot_login(page):
    """
    Security test (CRITICAL):
    Locked out user must NOT be able to log in
    even with valid credentials.
    """

    # =========================
    # Open login page
    # =========================
    with allure.step("Open login page"):
        login_page = LoginPage(page)
        await login_page.open()

    # =========================
    # Attempt login as locked_out_user
    # =========================
    with allure.step("Attempt login as locked_out_user"):
        await login_page.login(
            TestData.LOCKED_OUT_USER,
            TestData.PASSWORD,
        )

    # =========================
    # Assert error is visible
    # =========================
    with allure.step("Verify error message is displayed"):
        assert await login_page.is_error_visible(), \
            "Error message should be visible for locked out user"

    # =========================
    # Assert exact error message
    # =========================
    with allure.step("Verify exact error message text"):
        error_text = await login_page.get_error_text()
        assert error_text == (
            "Epic sadface: Sorry, this user has been locked out."
        ), f"Unexpected error message: {error_text}"

    # =========================
    # Assert access NOT granted
    # =========================
    with allure.step("Verify inventory page is NOT accessible"):
        assert "/inventory.html" not in page.url, \
            "Locked out user must not access inventory page"
