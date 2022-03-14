from vkbottle.bot import Blueprint, Message

from app.backend.classes.crud import ClassesREDIS
from app.vk_bot.blueprints.admin.rules import UpdateClassesDbRule

admin_bp = Blueprint()
redis = ClassesREDIS()


@admin_bp.on.message(UpdateClassesDbRule())
async def today_classes_filter(message: Message):
    await redis.reset_database()
