from config import settings
from vkbottle import Bot, run_multibot, API

from refactor.vk_bot.blueprints.binding import blueprints
from refactor.vk_bot.misc.middlewares import middlewares

bot = Bot(settings.DOMASHKA_TOKEN)
apis = (API(settings.DOMASHKA_TOKEN), API(settings.TEST_TOKEN))

[bp.load(bot) for bp in blueprints]
[bot.labeler.message_view.register_middleware(middleware) for middleware in middlewares]

run_multibot(bot, apis=apis)
