# core/base_page.py
from playwright.async_api import Page, Locator
from config.settings import Settings
from core.utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    async def goto(self, url: str):
        self.logger.info(f"Navigating to URL: {url}")
        await self.page.goto(url, timeout=Settings.TIMEOUT)

    async def wait_for_url(self, url_part: str):
        self.logger.info(f"Waiting for URL to contain: {url_part}")
        await self.page.wait_for_url(f"**{url_part}", timeout=Settings.TIMEOUT)

    async def wait_for_locator(self, locator: Locator):
        self.logger.info("Waiting for locator to be visible")
        await locator.wait_for(state="visible", timeout=Settings.TIMEOUT)

    async def click(self, locator: Locator):
        self.logger.info("Clicking on element")
        await self.wait_for_locator(locator)
        await locator.click()

    async def fill(self, locator: Locator, text: str):
        self.logger.info(f"Filling input with text: {text}")
        await self.wait_for_locator(locator)
        await locator.fill(text)

    async def get_text(self, locator: Locator) -> str:
        self.logger.info("Getting text from element")
        await self.wait_for_locator(locator)
        return await locator.inner_text()

    async def is_visible(self, locator: Locator) -> bool:
        visible = await locator.is_visible()
        self.logger.info(f"Element visible: {visible}")
        return visible

