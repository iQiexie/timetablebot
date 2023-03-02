from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.backend.db.deps import async_session
from app.backend.handlers.users.crud import UserCRUD
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(['count users']))
async def admin(message: Message):
    async with async_session() as session:
        count = await UserCRUD(session=session).get_daily_users()

    await message.answer(f'{count}')


@blueprint.on.message(ContainsTriggerRule(['get usercount']))
async def admin(message: Message):
    async with async_session() as session:
        rows = await UserCRUD(session=session).get_daily_users_by_day()

    result = ""
    for row in rows:
        result += str(row)

    await message.answer(f'{result}')


@blueprint.on.message(ContainsTriggerRule(['count by grades']))
async def admin(message: Message):
    async with async_session() as session:
        result = await UserCRUD(session=session).get_usercount_by_grade()

    await message.answer(f'{result}')
