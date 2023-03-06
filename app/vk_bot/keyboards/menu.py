from vkbottle import Keyboard, KeyboardButtonColor, Text

menu_keyboard = Keyboard(one_time=False, inline=False)
menu_keyboard.add(Text("🔎 Сегодняшние пары", {"cmd": "today"}), KeyboardButtonColor.PRIMARY)
menu_keyboard.add(Text("🔎 Завтрашние пары", {"cmd": "tomorrow"}), KeyboardButtonColor.PRIMARY)
menu_keyboard.row()
menu_keyboard.add(
    Text("Эта неделя", {"cmd": "sweek", "next": False}), KeyboardButtonColor.SECONDARY
)
menu_keyboard.add(
    Text("Следующая неделя", {"cmd": "sweek", "next": True}), KeyboardButtonColor.SECONDARY
)
menu_keyboard.row()
menu_keyboard.add(Text("🤖 ChatGPT", {"cmd": "chatgpt"}), KeyboardButtonColor.POSITIVE)
menu_keyboard.add(Text("🛠 Настройки", {"cmd": "settings"}), KeyboardButtonColor.SECONDARY)
menu_keyboard.row()
menu_keyboard.add(Text("Убрать клавиатуру", {"cmd": "suicide"}), KeyboardButtonColor.NEGATIVE)
