from vkbottle.bot import Message

from app.frontend.common.dto.user import User
from app.frontend.vk_bot.keyboards.settings.change_group import change_group_keyboard


async def group_index_set(message: Message, user: User) -> bool:
    if not user.group_number:
        text = 'Пожалуйста, укажи группу. Напиши "поменять группу" или нажми на кнопку внизу'
        await message.answer(text, keyboard=change_group_keyboard)
        return False

    return True
