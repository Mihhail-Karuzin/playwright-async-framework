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
#     # 🔒 Normalize browser option (CRITICAL for CI)
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
# # Context + VIDEO + TRACE (correct lifecycle)
# # =====================================================
# @pytest_asyncio.fixture
# async def context(request, browser_instance):
#     os.makedirs("artifacts/videos", exist_ok=True)
#     os.makedirs("artifacts/traces", exist_ok=True)
#
#     context = await browser_instance.new_context(
#         record_video_dir="artifacts/videos",
#         record_video_size={"width": 1280, "height": 720},
#     )
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
#     # 📦 TRACE — MUST be stopped BEFORE context.close()
#     if rep and rep.failed:
#         trace_path = (
#             f"artifacts/traces/"
#             f"{request.node.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
#         )
#         await context.tracing.stop(path=trace_path)
#     else:
#         await context.tracing.stop()
#
#     # 🔚 CLOSE CONTEXT → video finalized here
#     await context.close()
#
#     # 🎥 Attach VIDEO + TRACE to Allure (after close)
#     if rep and rep.failed:
#         try:
#             video_path = getattr(request.node, "video_path", None)
#             if video_path:
#                 allure.attach.file(
#                     video_path,
#                     name="Failure Video",
#                     attachment_type=AttachmentType.MP4,
#                 )
#
#             if rep and trace_path:
#                 allure.attach.file(
#                     trace_path,
#                     name="Playwright Trace",
#                     attachment_type=AttachmentType.ZIP,
#                 )
#         except Exception as e:
#             logger.warning(f"Failed to attach video/trace: {e}")
#
#
# # =====================================================
# # Page (video path must be saved BEFORE close)
# # =====================================================
# @pytest_asyncio.fixture
# async def page(request, context):
#     page = await context.new_page()
#     yield page
#
#     # 🎥 Save video path BEFORE page is closed
#     if page.video:
#         try:
#             request.node.video_path = await page.video.path()
#         except Exception:
#             pass
#
#     await page.close()
#
#
# # =====================================================
# # Allure fast attachments (SYNC, safe)
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
#             # 📸 Screenshot (bytes → Allure)
#             screenshot = loop.run_until_complete(page.screenshot())
#             allure.attach(
#                 screenshot,
#                 name="Failure Screenshot",
#                 attachment_type=AttachmentType.PNG,
#             )
#
#             # 🌐 URL
#             allure.attach(
#                 page.url,
#                 name="Current URL",
#                 attachment_type=AttachmentType.URI_LIST,
#             )
#
#             # ❌ Error
#             allure.attach(
#                 str(rep.longrepr),
#                 name="Error details",
#                 attachment_type=AttachmentType.TEXT,
#             )





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

        # Attach trace to Allure
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

            # Screenshot
            screenshot = loop.run_until_complete(page.screenshot())
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG,
            )

            # Current URL
            allure.attach(
                page.url,
                name="Current URL",
                attachment_type=AttachmentType.URI_LIST,
            )

            # Error details
            allure.attach(
                str(rep.longrepr),
                name="Error details",
                attachment_type=AttachmentType.TEXT,
            )


















