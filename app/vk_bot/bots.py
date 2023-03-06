from vkbottle import API
from vkbottle import Bot

from config import settings

__prod_bot = Bot(settings.VK_DOMASHKA_TOKEN)
__prod_apis = (API(settings.VK_DOMASHKA_TOKEN), API(settings.VK_RASPISANIE_TOKEN))

__test_bot = Bot(settings.VK_KPKPKP_TOKEN)
__test_apis = (API(settings.VK_KPKPKP_TOKEN),)

if settings.PRODUCTION:
    current_bot = __prod_bot
    current_apis = __prod_apis
else:
    current_bot = __test_bot
    current_apis = __test_apis
