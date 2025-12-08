# core/browser.py

from playwright.async_api import async_playwright
from config.settings import Settings

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None

    async def start_browser(self):
        """
        Запускает экземпляр браузера на основе настроек из Settings.
        Возвращает объект browser.
        """
        self.playwright = await async_playwright().start()
        self.browser = await getattr(self.playwright, Settings.BROWSER).launch(
            headless=Settings.HEADLESS
        )
        return self.browser

    async def stop_browser(self):
        """
        Закрывает браузер и Playwright, освобождая ресурсы.
        """
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


