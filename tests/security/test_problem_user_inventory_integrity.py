import pytest
import allure

from core.pages.login_page import LoginPage
from core.pages.inventory_page import InventoryPage
from tests.test_data import TestData


@pytest.mark.asyncio
@pytest.mark.security
@pytest.mark.xfail(
    reason=(
        "Known issue: problem_user sees broken inventory images. "
        "UI integrity is compromised."
    ),
    strict=False,
)
# @allure.severity(allure.severity_level.MAJOR)
@allure.severity(allure.severity_level.CRITICAL)

@allure.feature("Inventory")
@allure.story("Problem user inventory integrity")
async def test_problem_user_inventory_images_are_correct(page):
    """
    Security / UI integrity test:
    Inventory images must be correct and unique per product.

    Current SauceDemo behavior:
    - problem_user sees incorrect / duplicated images.
    """

    # =========================
    # Login as problem_user
    # =========================
    with allure.step("Login as problem_user"):
        login_page = LoginPage(page)
        await login_page.open()
        await login_page.login(
            TestData.PROBLEM_USER,
            TestData.PASSWORD,
        )

    # =========================
    # Open inventory page
    # =========================
    with allure.step("Open inventory page"):
        inventory_page = InventoryPage(page)
        await inventory_page.wait_for_inventory_page()

    # =========================
    # Collect product images
    # =========================
    with allure.step("Collect inventory product images"):
        images = await page.locator(".inventory_item_img img").all()

        image_sources = [
            await img.get_attribute("src")
            for img in images
        ]

    # =========================
    # Assertions (expected behavior)
    # =========================
    with allure.step("Verify images are unique and valid"):
        assert len(image_sources) > 0, "Inventory should contain product images"

        assert len(set(image_sources)) == len(image_sources), (
            "Each product should have a unique image. "
            "Duplicate images detected — UI integrity issue."
        )
