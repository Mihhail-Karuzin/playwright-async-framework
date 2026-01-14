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


# -------------------------------
# Browser
# -------------------------------
@pytest_asyncio.fixture
async def browser_instance(request):
    browser_name = request.config.getoption("browser") or "chromium"

    async with async_playwright() as p:
        headless = True if os.environ.get("CI") else Settings.HEADLESS
        browser = await getattr(p, browser_name).launch(headless=headless)

        yield browser
        await browser.close()


# -------------------------------
# Context + VIDEO + TRACE (CORRECT)
# -------------------------------
@pytest_asyncio.fixture
async def context(request, browser_instance):
    os.makedirs("artifacts/videos", exist_ok=True)
    os.makedirs("artifacts/traces", exist_ok=True)

    context = await browser_instance.new_context(
        record_video_dir="artifacts/videos",
        record_video_size={"width": 1280, "height": 720},
    )

    await context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield context

    rep = getattr(request.node, "rep_call", None)

    # 📦 TRACE — BEFORE close
    if rep and rep.failed:
        trace_path = (
            f"artifacts/traces/"
            f"{request.node.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
        )
        await context.tracing.stop(path=trace_path)
    else:
        await context.tracing.stop()

    # 🔚 CLOSE CONTEXT → VIDEO IS FINALIZED HERE
    await context.close()

    # 🎥 VIDEO — AFTER close
    if rep and rep.failed:
        try:
            video_path = request.node.video_path
            allure.attach.file(
                video_path,
                name="Failure Video",
                attachment_type=AttachmentType.MP4,
            )
            allure.attach.file(
                trace_path,
                name="Playwright Trace",
                attachment_type=AttachmentType.ZIP,
            )
        except Exception as e:
            logger.warning(f"Attach failed: {e}")


# -------------------------------
# Page
# -------------------------------
@pytest_asyncio.fixture
async def page(request, context):
    page = await context.new_page()
    yield page

    # save video path BEFORE page close
    if page.video:
        request.node.video_path = await page.video.path()

    await page.close()


# -------------------------------
# ALLURE FAST ATTACHMENTS
# -------------------------------
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

            loop = asyncio.get_event_loop()

            # 📸 Screenshot
            screenshot = loop.run_until_complete(page.screenshot())
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG,
            )

            # 🌐 URL
            allure.attach(
                page.url,
                name="Current URL",
                attachment_type=AttachmentType.URI_LIST,
            )

            # ❌ Error
            allure.attach(
                str(rep.longrepr),
                name="Error details",
                attachment_type=AttachmentType.TEXT,
            )






















