from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.vk_bot.rules.contains_trigger import ContainsTriggerRule

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=['admin']))
async def admin(message: Message):
    await message.answer('not implemented')
