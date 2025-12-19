# tests/regression/test_login.py

import pytest
from core.pages.login_page import LoginPage
from config.test_data import TestData

@pytest.mark.asyncio
async def test_login_success(page):
    """
    Test that valid user can log in and
    inventory page is displayed.
    """
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)

    assert await login_page.is_logged_in()
