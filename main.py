import asyncio
import logging
import os

from app.routines import actualize
from app.routines import count_users
from app.vk_bot.driver import run
from config import settings


def init_logger():
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger().handlers[0]
    log_format = "%(asctime)-15s | %(levelname).1s | %(name)8s |  %(message)s"
    logger.setFormatter(logging.Formatter(log_format))


init_logger()

if __name__ == "__main__":
    if os.getenv("ROUTINE") == "ACTUALIZE":
        print(f"Running actualize routine with {settings.PRODUCTION=}")
        asyncio.run(actualize())
    elif os.getenv("ROUTINE") == "REPORT":
        print(f"Running report routine with {settings.PRODUCTION=}")
        asyncio.run(count_users())
    else:
        print(f"Starting bot with {settings.PRODUCTION=}")
        run()
