from vkbottle.bot import Blueprint, Message

from refactor.vk_bot.blueprints.settings.rules import SettingsGeneralRule
from refactor.vk_bot.misc.keyboards import settings_keyboard

settings_bp = Blueprint()


@settings_bp.on.message(SettingsGeneralRule())
async def send_settings_keyboard(message: Message):
    await message.answer(keyboard=settings_keyboard)



