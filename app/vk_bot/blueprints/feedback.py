from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.backend.handlers.users.schemes import UserSchema
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule
from config import settings

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["downvote"]))
async def downvote(message: Message, user: UserSchema):
    """Отправляет админу о некорректной паре"""

    text = (
        f"Пользователю: https://vk.com/gim206763355?sel={user.vk_id} "
        f"Пришли невалидные пары. \n\nКонтекст:\n"
        f"{message.payload}"
    )

    answer_text = (
        "Обратная связь учтена, админ напишет как только у него появится свободное время. "
        "Спасибо за репорт 💖\n\n"
        "Наиболее частые причины неправильного расписания:\n\n"
        "1. Не та неделя - посмотри внимательно на дату присланных пар\n\n"
        "2. Неправильная группа - возможно, у тебя в настройках выставлен не тот номер группы\n\n"
        "3. Задержка в обновлении - расписание в боте обновляется раз в час. Возможно, учебка "
        "внесла изменения в расписание совсем недавно. Подожди часик, а потом проверь снова\n\n"
    )

    await message.ctx_api.messages.send(peer_ids=settings.VK_ADMIN_IDS, random_id=0, message=text)
    await message.answer(answer_text)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["upvote"]))
async def upvote(message: Message):
    """Ничего не делает, просто высылает фидбек юзверу"""

    await message.answer("Обратная связь учтена. Спасибо 💖")