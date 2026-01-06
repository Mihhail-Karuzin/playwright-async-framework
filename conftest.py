# conftest.py

import os
from datetime import datetime

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from config.settings import Settings


@pytest_asyncio.fixture
async def page(request):
    """
    Provide a Playwright Page object for tests.
    Supports browser as string or list (GitHub Actions matrix passes it as ['chromium']).
    Headless mode is enforced for CI.
    """

    # Получаем браузер из pytest
    browser_option = request.config.getoption("browser")
    if isinstance(browser_option, (list, tuple)):
        browser_name = browser_option[0]
    else:
        browser_name = browser_option

    # Headless из Settings или переменной окружения
    headless_env = os.getenv("HEADLESS", str(Settings.HEADLESS)).lower() == "true"

    async with async_playwright() as p:
        if browser_name.lower() == "chromium":
            browser = await p.chromium.launch(headless=headless_env)
        elif browser_name.lower() == "firefox":
            browser = await p.firefox.launch(headless=headless_env)
        elif browser_name.lower() == "webkit":
            browser = await p.webkit.launch(headless=headless_env)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        context = await browser.new_context()
        page_obj = await context.new_page()

        yield page_obj

        await browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Take a screenshot on test failure.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            screenshots_dir = "artifacts/screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name
            screenshot_file = f"{screenshots_dir}/{test_name}_{timestamp}.png"

            import asyncio
            loop = asyncio.get_event_loop()
            loop.run_until_complete(page.screenshot(path=screenshot_file))

















