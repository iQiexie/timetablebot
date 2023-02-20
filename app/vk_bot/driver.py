from typing import Iterable

from vkbottle import API
from vkbottle import Bot
from vkbottle import run_multibot

from app.vk_bot.blueprints import blueprints
from app.vk_bot.middlewares import middlewares
from config import settings


def start_bot(bot: Bot, apis: Iterable[API]):
    for blueprint in blueprints:
        blueprint.load(bot)

    for middleware in middlewares:
        bot.labeler.message_view.register_middleware(middleware)

    run_multibot(bot, apis=apis)


def run():
    if settings.PRODUCTION:
        bot = Bot(settings.VK_DOMASHKA_TOKEN)
        apis = (API(settings.VK_DOMASHKA_TOKEN), API(settings.VK_RASPISANIE_TOKEN))
    else:
        bot = Bot(settings.VK_KPKPKP_TOKEN)
        apis = (API(settings.VK_KPKPKP_TOKEN),)

    start_bot(bot=bot, apis=apis)
