import pytest
from core.browser import BrowserManager
from config.settings import Settings

@pytest.fixture
async def browser():
    manager = BrowserManager()
    browser = await manager.start_browser()
    yield browser
    await manager.stop_browser()

@pytest.fixture
async def page(browser):
    # Создаём контекст, можно задать viewport, если нужно
    context = await browser.new_context(viewport=Settings.WINDOW_SIZE)
    page = await context.new_page()
    yield page
    await context.close()

