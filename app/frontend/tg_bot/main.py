import logging

from aiogram.types import BotCommand

from app.frontend.clients.telegram import TelegramClient
from app.frontend.singletons import Clients
from app.frontend.tg_bot.binding import get_root_dispatcher


def init_logger() -> None:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger().handlers[0]
    log_format = "%(asctime)-15s | %(levelname).1s | %(name)8s |  %(message)s"
    logger.setFormatter(logging.Formatter(log_format))

    logging_logger = logging.getLogger()
    logging_logger.setLevel(level=logging.DEBUG)


async def start_telegram_bot() -> None:
    init_logger()

    await TelegramClient.bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Открыть меню бота"),
        ],
    )
    root_router = get_root_dispatcher()
    await root_router.start_polling(
        Clients.telegram.bot,
        allowed_updates=root_router.resolve_used_update_types(),
    )
