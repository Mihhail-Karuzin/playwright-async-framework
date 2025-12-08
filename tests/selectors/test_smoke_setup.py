import pytest
from core.base_page import BasePage

@pytest.mark.asyncio
async def test_setup(page):
    base_page = BasePage(page)
    await base_page.navigate("")  # переходим на BASE_URL
    title = await base_page.get_title()
    print("Page title:", title)
    await page.wait_for_timeout(2000)
    assert "Playwright" in title










