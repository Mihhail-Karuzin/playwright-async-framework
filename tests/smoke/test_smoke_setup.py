# tests/smoke/test_smoke_setup.py

import pytest
from core.pages.login_page import LoginPage

@pytest.mark.asyncio
async def test_smoke_setup(page):
    """
    Smoke test to ensure browser starts
    and the login page loads correctly.
    """
    login_page = LoginPage(page)
    await login_page.open()
    assert "saucedemo" in page.url
