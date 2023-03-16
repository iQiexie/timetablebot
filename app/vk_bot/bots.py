from vkbottle import API
from vkbottle import Bot

from config import settings

if settings.PRODUCTION:
    current_bot = Bot(settings.VK_DOMASHKA_TOKEN)
    current_apis = (API(settings.VK_DOMASHKA_TOKEN), API(settings.VK_RASPISANIE_TOKEN))
else:
    current_bot = Bot(settings.VK_KPKPKP_TOKEN)
    current_apis = (API(settings.VK_KPKPKP_TOKEN),)
