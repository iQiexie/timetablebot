from vkbottle import Keyboard, KeyboardButtonColor, Text

settings_keyboard = Keyboard(one_time=False, inline=False)
settings_keyboard.add(
    Text("👨‍👩‍👧‍👦 Поменять группу", payload={"cmd": "change group"}),
    color=KeyboardButtonColor.PRIMARY,
)
settings_keyboard.add(
    Text("⚙ Uptime расписания", payload={"cmd": "uptime"}),
    color=KeyboardButtonColor.PRIMARY,
)
settings_keyboard.row()
settings_keyboard.add(
    # Text("🙊 Виртуальный собеседник", payload={"cmd": "toggle chatbot"}),
    Text("📈 Статистика", payload={"cmd": "statistics"}),
    color=KeyboardButtonColor.PRIMARY,
)
settings_keyboard.row()
settings_keyboard.add(
    Text("В меню", payload={"cmd": "main menu"}),
    color=KeyboardButtonColor.NEGATIVE,
)
