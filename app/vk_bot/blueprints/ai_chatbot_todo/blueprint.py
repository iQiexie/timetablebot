from vkbottle.bot import Blueprint

settings_bp = Blueprint()

#
# @settings_bp.on.message(SettingsRule())
# async def send_settings_keyboard_handler(message: Message, user: UserSchema):
#     text = (
#                 f"Твоя/ваша группа: {user.group_index} \n\n"
#                 "Список команд:\n"
#                 "vk.com/@mpsu_schedule-vse-komandy-bota\n\n"
#                 "F.A.Q:\n"
#                 "https://vk.com/topic-206763355_48153565\n\n"
#                 "Если чё-то не работает, пиши мне @baboomka"
#     )
#
#     await message.answer(keyboard=settings_keyboard, message=text)