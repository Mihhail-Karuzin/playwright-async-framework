# tests/regression/test_login_negative.py

import pytest
from core.pages.login_page import LoginPage
from config.test_data import TestData

@pytest.mark.asyncio
async def test_login_invalid(page):
    """
    Test that invalid credentials show an error message.
    """
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(TestData.INVALID_USERNAME, TestData.INVALID_PASSWORD)

    assert await login_page.is_error_visible()
