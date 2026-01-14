import pytest

from core.pages.login_page import LoginPage
from core.utils.logger import get_logger

logger = get_logger("test_smoke_setup")


@pytest.mark.asyncio
async def test_smoke_setup(page):
    """
    Smoke test to ensure browser starts
    and the login page loads correctly.
    """

    logger.info("Starting smoke setup test")

    login_page = LoginPage(page)
    logger.info("LoginPage object created")

    await login_page.open()
    logger.info("Login page opened")

    await page.wait_for_url("**saucedemo.com**")

    current_url = page.url
    logger.info(f"Current URL after open: {current_url}")

    # ✅ NORMAL SMOKE ASSERT (production)
    assert "saucedemo" in current_url

    # ❌ BREAK TEST (use when you need to validate screenshots / allure / traces)
    # assert "this_will_fail" in current_url

    logger.info("Smoke setup test finished successfully")

