#
# import os
# import asyncio
# from datetime import datetime
#
# import pytest
# import pytest_asyncio
# from playwright.async_api import async_playwright
#
# from config.settings import Settings
# from core.utils.logger import get_logger
#
# import allure
# from allure_commons.types import AttachmentType
#
# logger = get_logger("pytest")
#
#
# # =====================================================
# # Browser (CI-safe, handles list from pytest-playwright)
# # =====================================================
# @pytest_asyncio.fixture
# async def browser_instance(request):
#     browser_option = request.config.getoption("browser")
#
#     # Normalize browser option (CRITICAL for CI)
#     if not browser_option:
#         browser_name = "chromium"
#     elif isinstance(browser_option, (list, tuple)):
#         browser_name = browser_option[0]
#     else:
#         browser_name = browser_option
#
#     async with async_playwright() as p:
#         headless = True if os.environ.get("CI") else Settings.HEADLESS
#
#         if browser_name == "chromium":
#             browser = await p.chromium.launch(headless=headless)
#         elif browser_name == "firefox":
#             browser = await p.firefox.launch(headless=headless)
#         elif browser_name == "webkit":
#             browser = await p.webkit.launch(headless=headless)
#         else:
#             raise ValueError(f"Unsupported browser: {browser_name}")
#
#         yield browser
#         await browser.close()
#
#
# # =====================================================
# # Context + Trace lifecycle (NO video)
# # =====================================================
# @pytest_asyncio.fixture
# async def context(request, browser_instance):
#     os.makedirs("artifacts/traces", exist_ok=True)
#
#     context = await browser_instance.new_context()
#
#     await context.tracing.start(
#         screenshots=True,
#         snapshots=True,
#         sources=True,
#     )
#
#     yield context
#
#     rep = getattr(request.node, "rep_call", None)
#
#     if rep and rep.failed:
#         trace_path = (
#             f"artifacts/traces/"
#             f"{request.node.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
#         )
#         await context.tracing.stop(path=trace_path)
#
#         # Attach trace to Allure
#         allure.attach.file(
#             trace_path,
#             name="Playwright Trace",
#             attachment_type=AttachmentType.ZIP,
#         )
#     else:
#         await context.tracing.stop()
#
#     await context.close()
#
#
# # =====================================================
# # Page
# # =====================================================
# @pytest_asyncio.fixture
# async def page(context):
#     page = await context.new_page()
#     yield page
#     await page.close()
#
#
# # =====================================================
# # Allure attachments (FAST + SAFE)
# # =====================================================
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#
#     if rep.when == "call":
#         item.rep_call = rep
#
#         if rep.failed:
#             page = item.funcargs.get("page")
#             if not page:
#                 return
#
#             logger.error(f"Test failed: {item.name}")
#
#             loop = asyncio.get_event_loop()
#
#             # Screenshot
#             screenshot = loop.run_until_complete(page.screenshot())
#             allure.attach(
#                 screenshot,
#                 name="Failure Screenshot",
#                 attachment_type=AttachmentType.PNG,
#             )
#
#             # Current URL
#             allure.attach(
#                 page.url,
#                 name="Current URL",
#                 attachment_type=AttachmentType.URI_LIST,
#             )
#
#             # Error details
#             allure.attach(
#                 str(rep.longrepr),
#                 name="Error details",
#                 attachment_type=AttachmentType.TEXT,
#             )
#





import os
import asyncio
from datetime import datetime

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

from config.settings import Settings
from core.utils.logger import get_logger

import allure
from allure_commons.types import AttachmentType

logger = get_logger("pytest")


# =====================================================
# Browser (CI-safe, handles list from pytest-playwright)
# =====================================================
@pytest_asyncio.fixture
async def browser_instance(request):
    browser_option = request.config.getoption("browser")

    # Normalize browser option (CRITICAL for CI)
    if not browser_option:
        browser_name = "chromium"
    elif isinstance(browser_option, (list, tuple)):
        browser_name = browser_option[0]
    else:
        browser_name = browser_option

    async with async_playwright() as p:
        headless = True if os.environ.get("CI") else Settings.HEADLESS

        if browser_name == "chromium":
            browser = await p.chromium.launch(headless=headless)
        elif browser_name == "firefox":
            browser = await p.firefox.launch(headless=headless)
        elif browser_name == "webkit":
            browser = await p.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        yield browser
        await browser.close()


# =====================================================
# Context + Trace lifecycle (NO video)
# =====================================================
@pytest_asyncio.fixture
async def context(request, browser_instance):
    os.makedirs("artifacts/traces", exist_ok=True)

    context = await browser_instance.new_context()

    await context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield context

    rep = getattr(request.node, "rep_call", None)

    if rep and rep.failed:
        trace_path = (
            f"artifacts/traces/"
            f"{request.node.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
        )
        await context.tracing.stop(path=trace_path)

        allure.attach.file(
            trace_path,
            name="Playwright Trace",
            attachment_type=AttachmentType.ZIP,
        )
    else:
        await context.tracing.stop()

    await context.close()


# =====================================================
# Page
# =====================================================
@pytest_asyncio.fixture
async def page(context):
    page = await context.new_page()
    yield page
    await page.close()


# =====================================================
# Allure attachments (FAST + SAFE)
# =====================================================
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        item.rep_call = rep

        if rep.failed:
            page = item.funcargs.get("page")
            if not page:
                return

            logger.error(f"Test failed: {item.name}")

            loop = asyncio.get_event_loop()

            # 📸 Screenshot
            screenshot = loop.run_until_complete(page.screenshot())
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG,
            )

            # 🌐 Current URL
            allure.attach(
                page.url,
                name="Current URL",
                attachment_type=AttachmentType.URI_LIST,
            )

            # ❌ Error details
            allure.attach(
                str(rep.longrepr),
                name="Error details",
                attachment_type=AttachmentType.TEXT,
            )


# =====================================================
# AUTH FIXTURES (Phase 1.5.1)
# =====================================================
@pytest_asyncio.fixture
async def login_as(page):
    """
    Factory fixture for logging in as a specific user.

    Usage:
        await login_as(username, password)
    """
    from core.pages.login_page import LoginPage

    async def _login(username: str, password: str):
        login_page = LoginPage(page)
        await login_page.open()
        await login_page.login(username, password)
        return page

    return _login


@pytest_asyncio.fixture
async def logged_in_page(page):
    """
    Logged-in page using default valid user.
    """
    from core.pages.login_page import LoginPage

    login_page = LoginPage(page)
    await login_page.open()
    await login_page.login(
        Settings.VALID_USERNAME,
        Settings.VALID_PASSWORD,
    )

    return page














