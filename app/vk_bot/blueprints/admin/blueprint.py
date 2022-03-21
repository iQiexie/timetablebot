import asyncbg
from vkbottle.bot import Blueprint, Message
import multiprocessing as mp

from app.vk_bot.actualizer_utils import class_updater
from app.vk_bot.blueprints.admin.rules import UpdateClassesDbRule

admin_bp = Blueprint()


@admin_bp.on.message(UpdateClassesDbRule())
async def admin(message: Message):
    await message.answer('added task')
    await asyncbg.call(class_updater)
