# tests/feature/test_logout.py

import pytest
from core.pages.login_page import LoginPage
from core.pages.header_page import HeaderPage
from config.test_data import TestData

@pytest.mark.asyncio
async def test_logout(page):
    """
    Test that user can log out
    and returns to the login page.
    """
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)

    header_page = HeaderPage(page)
    await header_page.logout()

    # Verify that user is back on login page
    assert await page.locator('[data-test="login-button"]').is_visible()
    assert page.url.rstrip("/").endswith("saucedemo.com")
