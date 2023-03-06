from vkbottle import Keyboard, KeyboardButtonColor, Text
from app.vk_bot.blueprints.chat_gpt.states import ChatGptStates


def get_gpt_keyboard(state: ChatGptStates):
    gpt_keyboard = Keyboard(one_time=False, inline=False)
    gpt_keyboard.row()

    if state == ChatGptStates.WAITING_FOR_ANSWER:
        gpt_keyboard.add(
            Text("⏳ Ожидание ответа", {"cmd": "gpt_status"}),
            KeyboardButtonColor.SECONDARY,
        )
        gpt_keyboard.row()
    elif state == ChatGptStates.CHATTING:
        gpt_keyboard.add(
            Text("🟢 Ожидание сообщения", {"cmd": "gpt_status"}),
            KeyboardButtonColor.SECONDARY,
        )
        gpt_keyboard.row()
    elif state == ChatGptStates.NOT_CHATTING:
        gpt_keyboard.add(
            Text("❌ ChatGPT выключен", {"cmd": "gpt_status"}),
            KeyboardButtonColor.SECONDARY,
        )
        gpt_keyboard.row()

    gpt_keyboard.add(
        Text("🔴 Остановить диалог", {"cmd": "gpt stop"}),
        KeyboardButtonColor.PRIMARY,
    )
    gpt_keyboard.add(
        Text("🟢 Возобновить диалог", {"cmd": "chatgpt"}),
        KeyboardButtonColor.PRIMARY,
    )
    gpt_keyboard.row()
    gpt_keyboard.add(
        Text("🗑 Удалить диалог (В разработке)", {"cmd": "gpt delete"}),
        KeyboardButtonColor.PRIMARY,
    )
    gpt_keyboard.row()
    gpt_keyboard.add(
        Text("В меню", payload={"cmd": "main menu"}),
        color=KeyboardButtonColor.NEGATIVE,
    )

    return gpt_keyboard
