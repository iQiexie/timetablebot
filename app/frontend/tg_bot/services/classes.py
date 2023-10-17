from datetime import datetime
from datetime import timedelta
from typing import Optional

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from app.frontend.clients.request_clients import RequestClients
from app.frontend.clients.telegram import TelegramClient
from app.frontend.common.dto.user import User
from app.frontend.common.service import compose_classes
from app.frontend.tg_bot.keyboards.feedback import get_feedback_keyboard
from app.frontend.tg_bot.keyboards.settings import get_change_group_keyboard
from app.frontend.tg_bot.misc.callbacks import CallbackActions


async def group_index_set(message: CallbackQuery | Message, user: User) -> bool:
    if isinstance(message, CallbackQuery):
        message_id = message.message.message_id
    else:
        message_id = message.message_id

    if not user.group_number:
        text = "Пожалуйста, укажи группу. Для этого нажми на кнопку внизу 👇"
        await TelegramClient.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=message_id,
            text=text,
            reply_markup=get_change_group_keyboard(),
        )
        return False

    return True


def get_searching_date(
    searching_week_day: int,
    next_week: bool,
) -> datetime:
    current_week_day = datetime.now().isocalendar().weekday

    if searching_week_day == current_week_day:
        delta = 0
    else:
        delta = searching_week_day - current_week_day

    searching_date = datetime.now() + timedelta(days=delta)

    if next_week:
        searching_date += timedelta(days=7)

    return searching_date


async def send_by_day(
    query: CallbackQuery | Message,
    searching_date: datetime,
    current_user: User,
    state: FSMContext,
    back: CallbackActions,
    back_payload: Optional[dict] = None,
    is_webapp: Optional[bool] = False,
) -> None:
    context_data = await state.get_data()
    pattern = context_data.get("pattern")

    if not pattern and not await group_index_set(message=query, user=current_user):
        return

    final_message = await compose_classes(
        group_number=current_user.group_number,
        searching_date=searching_date,
        pattern=pattern,
        user_id=current_user.id,
        backend_client=RequestClients.tg_backend,
        is_webapp=is_webapp,
    )

    keyboard = get_feedback_keyboard(
        searching_date=searching_date.timestamp(),
        back=back,
        back_payload=back_payload,
    )

    await TelegramClient.send_message(
        message=query.message,
        text=final_message,
        reply_markup=keyboard,
    )

    context_data["back"] = back
    context_data["back_payload"] = back_payload
    await state.set_data(context_data)
