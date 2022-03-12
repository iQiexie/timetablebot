import logging
from config import settings

logging.basicConfig(level=settings.logging_level)


def get_logger(name: str, level=None):
    logger = logging.getLogger(f" {name} ")
    logger.setLevel(level=level or settings.logging_level)

    return logger
