# import os
# import allure
# from allure_commons.types import AttachmentType
#
#
# def attach_text(name: str, content: str):
#     """
#     Attach plain text to Allure report.
#     """
#     allure.attach(
#         content,
#         name=name,
#         attachment_type=AttachmentType.TEXT
#     )
#
#
# def attach_url(url: str):
#     """
#     Attach current URL as a clickable link in Allure.
#     """
#     allure.attach(
#         url,
#         name="Current URL",
#         attachment_type=AttachmentType.URI_LIST
#     )
#
#
# async def attach_screenshot_from_file(path: str, name: str = "Screenshot"):
#     """
#     Attach an existing screenshot file to Allure.
#     """
#     if not os.path.exists(path):
#         return
#
#     with open(path, "rb") as f:
#         allure.attach(
#             f.read(),
#             name=name,
#             attachment_type=AttachmentType.PNG
#         )
#
#
# def attach_file(
#     path: str,
#     name: str,
#     attachment_type: AttachmentType = AttachmentType.ZIP
# ):
#     """
#     Attach any file (trace, video, zip, etc.) to Allure.
#     """
#     if not os.path.exists(path):
#         return
#
#     with open(path, "rb") as f:
#         allure.attach(
#             f.read(),
#             name=name,
#             attachment_type=attachment_type
#         )





import allure
from allure_commons.types import AttachmentType


def attach_text(name: str, content: str):
    """
    Attach plain text to Allure report.
    """
    allure.attach(
        content,
        name=name,
        attachment_type=AttachmentType.TEXT
    )


def attach_url(url: str):
    """
    Attach current URL as clickable link in Allure.
    """
    allure.attach(
        url,
        name="Current URL",
        attachment_type=AttachmentType.URI_LIST
    )


def attach_screenshot_from_file(path: str, name: str = "Failure Screenshot"):
    """
    Attach screenshot image (PNG) to Allure from file.
    IMPORTANT: uses attach.file + PNG type
    """
    allure.attach.file(
        path,
        name=name,
        attachment_type=AttachmentType.PNG
    )


def attach_file(path: str, name: str = "Attachment"):
    """
    Attach any file (e.g. Playwright trace ZIP) to Allure.
    """
    allure.attach.file(
        path,
        name=name,
        attachment_type=AttachmentType.ZIP
    )
