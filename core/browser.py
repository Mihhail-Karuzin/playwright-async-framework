# core/browser.py

from playwright.async_api import async_playwright, Browser
from config.settings import Settings

class BrowserManager:
    async def start_browser(self) -> Browser:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=Settings.HEADLESS)
        return browser
