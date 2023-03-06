from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.backend.db.deps import async_session
from app.backend.handlers.users.crud import UserCRUD
from app.vk_bot.keyboards.statistics import statistics_keyboard
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["statistics"]))
async def statistics(message: Message):
    text = (
        "Добро пожаловать в статистику! В этом разделе можно узнать "
        "количество пользователей этого бота по разным классификациям"
    )

    await message.answer(text, keyboard=statistics_keyboard)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["usercount"]))
async def usercount(message: Message):
    async with async_session() as session:
        count = await UserCRUD(session=session).get_daily_users()
    await message.answer(f"{count}")


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["daily_usercount"]))
async def daily(message: Message):
    async with async_session() as session:
        rows = await UserCRUD(session=session).get_daily_users_by_day()

    result = ""
    for row in rows:
        result += str(row)

    await message.answer(f"{result}")


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["grade_usercount"]))
async def grade(message: Message):
    async with async_session() as session:
        result = await UserCRUD(session=session).get_usercount_by_grade()

    answer = ""

    for key, vale in result.items():
        answer += f"{key}: {vale}\n"

    await message.answer(answer)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["group_usercount"]))
async def group(message: Message):
    async with async_session() as session:
        result = await UserCRUD(session=session).get_usercount_by_groups()

    answer = ""
    for mapping in result:
        group_index = mapping["group_index"]
        count = mapping["count"]

        answer += f"Группа: {group_index}, Кол-во: {count}\n"

    await message.answer(answer)
