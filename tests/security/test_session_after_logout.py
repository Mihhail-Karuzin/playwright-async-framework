import pytest

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from core.pages.header_page import HeaderPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
async def test_protected_pages_after_logout_redirect(page):
    """
    Security test:
    After logout user must NOT be able
    to access protected pages directly.
    """

    # =========================
    # Login
    # =========================
    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        TestData.VALID_USERNAME,
        TestData.VALID_PASSWORD,
    )

    # =========================
    # Ensure logged in
    # =========================
    inventory_page = InventoryPage(page)
    await inventory_page.wait_for_inventory_page()

    # =========================
    # Logout
    # =========================
    header = HeaderPage(page)
    await header.logout()

    # =========================
    # Try accessing protected pages
    # =========================
    protected_urls = [
        "/inventory.html",
        "/cart.html",
        "/checkout-step-one.html",
        "/checkout-step-two.html",
        "/checkout-complete.html",
    ]

    for url in protected_urls:
        await page.goto(f"https://www.saucedemo.com{url}")

        assert (
            page.url.endswith("/")
            or "login" in page.url
        ), f"User should not access {url} after logout"
