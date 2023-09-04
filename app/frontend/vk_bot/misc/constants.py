from vkbottle import API
from vkbottle import Bot

from config import settings


TODAY_CLASSES_TRIGGERS = [
    "сегодняшние",
    "сегодня",
    "сёдня",
    "седня",
    "сейчас",
    "щас",
]

TOMORROW_CLASSES_TRIGGERS = [
    "завтра",
    "завтрашние",
]

SETTINGS_TRIGGERS = [
    "настройки",
    "settings",
]

CHANGE_GROUP_TRIGGERS = [
    "поменять группу",
    "выбрать группу",
    "сменить группу",
]


MENU_TRIGGERS = [
    "в меню",
    "главное меню",
    "начать",
    "покежь клаву",
    "клава",
    "start",
    "старт",
]


if settings.PRODUCTION:
    current_bot = Bot(settings.VK_DOMASHKA_TOKEN)
    current_apis = (API(settings.VK_DOMASHKA_TOKEN), API(settings.VK_RASPISANIE_TOKEN))
else:
    current_bot = Bot(settings.VK_KPKPKP_TOKEN)
    current_apis = (API(settings.VK_KPKPKP_TOKEN),)
