import pytest
from core.pages.login_page import LoginPage
from core.pages.header_page import HeaderPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
async def test_protected_page_after_logout_redirects(page):
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        TestData.VALID_USERNAME,
        TestData.VALID_PASSWORD
    )

    header = HeaderPage(page)
    await header.logout()

    await page.goto("https://www.saucedemo.com/inventory.html")

    assert await login_page.is_on_login_page()
