from vkbottle import Keyboard, KeyboardButtonColor, Text

change_group_keyboard = Keyboard(inline=True)
change_group_keyboard.add(Text("Поменять группу", payload={"cmd": "change group"}), color=KeyboardButtonColor.PRIMARY)


menu_keyboard = Keyboard(one_time=True, inline=False)
menu_keyboard.add(Text("Сегодняшние пары", payload={"cmd": "today"}), color=KeyboardButtonColor.PRIMARY)
menu_keyboard.add(Text("Завтрашние пары", payload={"cmd": "tomorrow"}), color=KeyboardButtonColor.PRIMARY)
menu_keyboard.row()
menu_keyboard.add(Text("Эта неделя", payload={"cmd": "this week"}), color=KeyboardButtonColor.SECONDARY)
menu_keyboard.add(Text("Настройки", payload={"cmd": "settings"}), color=KeyboardButtonColor.SECONDARY)
menu_keyboard.add(Text("Следующая неделя", payload={"cmd": "next week"}), color=KeyboardButtonColor.SECONDARY)
menu_keyboard.row()
menu_keyboard.add(Text("Убрать клавиатуру", payload={"cmd": "suicide"}), color=KeyboardButtonColor.NEGATIVE)
