import pytest
from core.pages.login_page import LoginPage

PROTECTED_URLS = [
    "/inventory.html",
    "/cart.html",
    "/checkout-step-one.html",
    "/checkout-step-two.html",
    "/checkout-complete.html",
]


@pytest.mark.asyncio
@pytest.mark.security
@pytest.mark.parametrize("path", PROTECTED_URLS)
async def test_protected_pages_redirect_to_login(page, path):
    await page.goto(f"https://www.saucedemo.com{path}")

    login_page = LoginPage(page)

    assert await login_page.is_on_login_page(), (
        f"Access to {path} should redirect to login page"
    )
