from vkbottle.bot import Blueprint, Message

from actualizer import redis
from app.backend.classes.handlers import scrape_spreadsheet
from app.vk_bot.blueprints.admin.rules import UpdateClassesDbRule

admin_bp = Blueprint()


@admin_bp.on.message(UpdateClassesDbRule())
async def admin(message: Message):
    await message.answer('started')

    day_schemas = await scrape_spreadsheet()
    await redis.reset_database(day_schemas)

    await message.answer('finished')
