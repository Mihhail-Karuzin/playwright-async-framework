import allure
from allure_commons.types import AttachmentType


def attach_text(name: str, content: str):
    allure.attach(
        content,
        name=name,
        attachment_type=AttachmentType.TEXT
    )


def attach_url(url: str):
    allure.attach(
        url,
        name="Current URL",
        attachment_type=AttachmentType.URI_LIST
    )


async def attach_screenshot_from_file(path: str, name: str = "Screenshot"):
    with open(path, "rb") as f:
        allure.attach(
            f.read(),
            name=name,
            attachment_type=AttachmentType.PNG
        )
