import asyncbg
from vkbottle.bot import Blueprint, Message
from app.vk_bot.blueprints.admin.rules import UpdateClassesDbRule

admin_bp = Blueprint()


@admin_bp.on.message(UpdateClassesDbRule())
async def admin(message: Message):
    await message.answer('not implemented')
