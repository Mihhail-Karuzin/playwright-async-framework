# conftest.py

import os
from datetime import datetime

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from config.settings import Settings


def pytest_addoption(parser):
    """
    Add custom CLI options:
    --browser: chromium, firefox, webkit
    --headless: true/false
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium, firefox, webkit"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="True",
        help="Headless mode: True or False"
    )


@pytest_asyncio.fixture
async def page(request):
    """
    Creates browser page based on CLI options
    """
    browser_name = request.config.getoption("--browser").lower()
    headless_flag = request.config.getoption("--headless").lower() == "true"

    async with async_playwright() as p:
        browser = None
        if browser_name == "chromium":
            browser = await p.chromium.launch(headless=headless_flag)
        elif browser_name == "firefox":
            browser = await p.firefox.launch(headless=headless_flag)
        elif browser_name == "webkit":
            browser = await p.webkit.launch(headless=headless_flag)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        context = await browser.new_context()
        page = await context.new_page()
        yield page

        await browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Screenshot-on-failure hook
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








