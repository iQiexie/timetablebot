import logging
from config import settings

logging.basicConfig(level=settings.logging_level)


def get_logger(name: str, level=None):
    logger = logging.getLogger(f" {name} ")
    logger.setLevel(level=level or settings.logging_level)

    return logger


def list_contains_str(message: str, triggers: list[str]) -> bool:
    for trigger in triggers:
        if trigger in message.lower():
            return True
