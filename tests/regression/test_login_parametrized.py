import pytest

from config.settings import Settings
from core.pages.login_page import LoginPage


# =====================================================
# VALID LOGIN CASES
# =====================================================
@pytest.mark.asyncio
@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password",
    [
        (Settings.VALID_USERNAME, Settings.VALID_PASSWORD),
    ],
)
async def test_login_valid_users(page, login_as, username, password):
    await login_as(username, password)

    login_page = LoginPage(page)
    assert await login_page.is_logged_in(), "User should be logged in"


# =====================================================
# INVALID LOGIN CASES
# =====================================================
@pytest.mark.asyncio
@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password",
    [
        ("", ""),                         # both empty
        ("wrong_user", "wrong_pass"),     # both invalid
        (Settings.VALID_USERNAME, ""),    # empty password
        ("", Settings.VALID_PASSWORD),    # empty username
        ("locked_out_user", "secret_sauce"),  # locked user
    ],
)
async def test_login_invalid_users(page, login_as, username, password):
    await login_as(username, password)

    login_page = LoginPage(page)
    assert await login_page.is_error_visible(), "Error message should be visible"


# =====================================================
# ERROR MESSAGE CONTENT (OPTIONAL BUT STRONG)
# =====================================================
@pytest.mark.asyncio
@pytest.mark.regression
async def test_login_error_message_text(page, login_as):
    await login_as("wrong_user", "wrong_pass")

    login_page = LoginPage(page)
    error_text = await login_page.get_error_text()

    assert "Username and password do not match" in error_text
