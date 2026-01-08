# # conftest.py
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



# conftest.py

# conftest.py

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
#         # Определяем headless режим
#         # На CI принудительно headless
#         headless = True if os.environ.get("CI") else Settings.HEADLESS
#
#         # Запуск нужного браузера
#         if browser_name.lower() == "chromium":
#             browser = await p.chromium.launch(headless=headless)
#         elif browser_name.lower() == "firefox":
#             args = ["--no-sandbox"] if os.environ.get("CI") else []
#             browser = await p.firefox.launch(headless=headless, args=args)
#         elif browser_name.lower() == "webkit":
#             browser = await p.webkit.launch(headless=headless)
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





import os
from datetime import datetime

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from config.settings import Settings


# -------------------------------
# Launch browser instance
# -------------------------------
@pytest_asyncio.fixture
async def browser_instance(request):
    """
    Launch a browser instance based on --browser option (default: chromium)
    """

    browser_option = request.config.getoption("browser")

    # Normalize browser value
    if not browser_option:
        browser_name = "chromium"  # default fallback
    elif isinstance(browser_option, (list, tuple)):
        browser_name = browser_option[0]
    else:
        browser_name = browser_option

    async with async_playwright() as p:
        # Headless forced in CI, configurable locally
        headless = True if os.environ.get("CI") else Settings.HEADLESS

        if browser_name.lower() == "chromium":
            browser = await p.chromium.launch(headless=headless)

        elif browser_name.lower() == "firefox":
            args = ["--no-sandbox"] if os.environ.get("CI") else []
            browser = await p.firefox.launch(headless=headless, args=args)

        elif browser_name.lower() == "webkit":
            browser = await p.webkit.launch(headless=headless)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        yield browser
        await browser.close()


# -------------------------------
# Create new context
# -------------------------------
@pytest_asyncio.fixture
async def context(browser_instance):
    context = await browser_instance.new_context()
    yield context
    await context.close()


# -------------------------------
# Create new page
# -------------------------------
@pytest_asyncio.fixture
async def page(context):
    page = await context.new_page()
    yield page


# -------------------------------
# Screenshot on failure
# -------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Take a screenshot if a test fails.
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



















