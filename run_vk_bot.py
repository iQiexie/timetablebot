from typing import Iterable

from vkbottle import API, Bot, run_multibot

from app.frontend.vk_bot.blueprints import blueprints
from app.frontend.vk_bot.middlewares import middlewares
from app.frontend.vk_bot.misc.constants import current_apis, current_bot
from main import init_logger


def start_bot(bot: Bot, apis: Iterable[API]) -> None:
    for blueprint in blueprints:
        blueprint.load(bot)

    for middleware in middlewares:
        bot.labeler.message_view.register_middleware(middleware)

    run_multibot(bot, apis=apis)


def run() -> None:
    start_bot(bot=current_bot, apis=current_apis)


if __name__ == "__main__":
    init_logger()
    run()
