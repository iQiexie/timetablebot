import json

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.backend.api.routes.dto.classes.request import RateRequest
from app.frontend.dto.user import User
from app.frontend.vk_bot.misc.contains_trigger_rule import ContainsTriggerRule
from app.frontend.vk_bot.misc.request_clients import RequestClients
from config import settings

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["downvote"]))
async def downvote(message: Message, user: User) -> None:
    """Отправляет админу о некорректной паре"""

    payload = json.loads(message.payload)
    requested_date = payload["srf"]
    pattern = payload.get("ptr")

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
    await RequestClients.backend.rate_class(
        data=RateRequest(
            date=requested_date,
            correct=False,
            vk_id=message.peer_id,
            pattern=pattern,
        )
    )


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["upvote"]))
async def upvote(message: Message) -> None:
    payload = json.loads(message.payload)
    requested_date = payload["srf"]
    pattern = payload.get("ptr")

    await message.answer("Обратная связь учтена. Спасибо 💖")
    await RequestClients.backend.rate_class(
        data=RateRequest(
            date=requested_date,
            correct=True,
            vk_id=message.peer_id,
            pattern=pattern,
        )
    )
