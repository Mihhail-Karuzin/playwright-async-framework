# conftest.py
#
# import os
# from datetime import datetime
#
# import pytest
# import pytest_asyncio
# from playwright.async_api import async_playwright
# from config.settings import Settings
#
#
# @pytest_asyncio.fixture
# async def page(request):
#     """
#     Provide a Playwright Page object for tests.
#     Handles browser_name as list or string (GitHub Actions passes it as ['chromium']).
#     """
#
#     # Получаем опцию browser из pytest-playwright
#     browser_option = request.config.getoption("browser")
#
#     # Если это список, берем первый элемент
#     if isinstance(browser_option, (list, tuple)):
#         browser_name = browser_option[0]
#     else:
#         browser_name = browser_option
#
#     async with async_playwright() as p:
#         browser = None
#
#         # Запуск нужного браузера
#         if browser_name.lower() == "chromium":
#             browser = await p.chromium.launch(headless=Settings.HEADLESS)
#         elif browser_name.lower() == "firefox":
#             browser = await p.firefox.launch(headless=Settings.HEADLESS)
#         elif browser_name.lower() == "webkit":
#             browser = await p.webkit.launch(headless=Settings.HEADLESS)
#         else:
#             raise ValueError(f"Unsupported browser: {browser_name}")
#
#         context = await browser.new_context()
#         page_obj = await context.new_page()
#
#         yield page_obj
#
#         await browser.close()
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """
#     Take a screenshot if a test fails.
#     """
#     outcome = yield
#     rep = outcome.get_result()
#
#     if rep.when == "call" and rep.failed:
#         page = item.funcargs.get("page")
#         if page:
#             screenshots_dir = "artifacts/screenshots"
#             os.makedirs(screenshots_dir, exist_ok=True)
#             timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             test_name = item.name
#             screenshot_file = f"{screenshots_dir}/{test_name}_{timestamp}.png"
#
#             import asyncio
#             loop = asyncio.get_event_loop()
#             loop.run_until_complete(page.screenshot(path=screenshot_file))


import pytest
from playwright.async_api import async_playwright

@pytest.fixture(scope="session")
async def browser_type(request):
    """Возвращает браузер для тестов из параметра --browser"""
    browser_name = request.config.getoption("--browser")
    async with async_playwright() as pw:
        if browser_name == "chromium":
            browser = await pw.chromium.launch(headless=True)
        elif browser_name == "firefox":
            browser = await pw.firefox.launch(headless=True, args=["--no-sandbox"])
        elif browser_name == "webkit":
            browser = await pw.webkit.launch(headless=True)
        else:
            raise ValueError(f"Unknown browser: {browser_name}")
        yield browser
        await browser.close()

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to run tests against: chromium, firefox, webkit"
    )



















