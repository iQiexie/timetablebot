from config import settings
from vkbottle import Bot, run_multibot, API

from refactor.base import get_logger
from refactor.vk_bot.blueprints import blueprints
from refactor.vk_bot.middlewares import middlewares

logger = get_logger("MAIN")
bot = Bot(settings.DOMASHKA_TOKEN)

apis = (
    API(settings.DOMASHKA_TOKEN),
    API(settings.TEST_TOKEN)
)

for bp in blueprints:
    bp.load(bot)

for middleware in middlewares:
    bot.labeler.message_view.register_middleware(middleware)

run_multibot(bot, apis=apis)
