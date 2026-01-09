# import logging
# import os
# from datetime import datetime
#
# LOG_DIR = "artifacts/logs"
# os.makedirs(LOG_DIR, exist_ok=True)
#
# def get_logger(name: str) -> logging.Logger:
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)
#
#     if logger.handlers:
#         return logger
#
#     timestamp = datetime.now().strftime("%Y-%m-%d")
#     log_file = os.path.join(LOG_DIR, f"{timestamp}.log")
#
#     formatter = logging.Formatter(
#         "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
#     )
#
#     file_handler = logging.FileHandler(log_file, encoding="utf-8")
#     file_handler.setFormatter(formatter)
#
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(formatter)
#
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
#
#     return logger



import logging
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("artifacts/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _get_log_level() -> int:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level, logging.INFO)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(_get_log_level())
    logger.propagate = False

    if logger.handlers:
        return logger

    log_file = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
