# core/base_page.py
from playwright.async_api import Page
from config.settings import Settings

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def navigate(self, path: str = ""):
        url = Settings.BASE_URL.rstrip("/") + "/" + path.lstrip("/")
        await self.page.goto(url)

    async def get_title(self) -> str:
        return await self.page.title()

    async def screenshot(self, path: str):
        await self.page.screenshot(path=path)
