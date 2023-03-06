from typing import Iterable

from vkbottle import API
from vkbottle import Bot
from vkbottle import run_multibot

from app.vk_bot.blueprints import blueprints
from app.vk_bot.bots import current_apis
from app.vk_bot.bots import current_bot
from app.vk_bot.middlewares import middlewares


def start_bot(bot: Bot, apis: Iterable[API]):
    for blueprint in blueprints:
        blueprint.load(bot)

    for middleware in middlewares:
        bot.labeler.message_view.register_middleware(middleware)

    run_multibot(bot, apis=apis)


def run():
    start_bot(bot=current_bot, apis=current_apis)
