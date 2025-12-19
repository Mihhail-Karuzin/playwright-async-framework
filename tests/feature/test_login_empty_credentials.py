# tests/feature/test_login_empty_credentials.py

import pytest
from core.pages.login_page import LoginPage

@pytest.mark.asyncio
async def test_login_empty_credentials(page):
    """
    Test that submitting empty credentials
    displays an error message.
    """
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login("", "")

    assert await login_page.is_error_visible()
