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

NOT_EXISTING_GROUPS = [410, 227]


current_bot = Bot(settings.VK_TOKEN)
current_apis = (API(settings.VK_TOKEN),)
