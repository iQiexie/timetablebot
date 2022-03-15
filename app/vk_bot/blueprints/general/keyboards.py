from vkbottle import Keyboard, KeyboardButtonColor, Text

change_group_keyboard = Keyboard(inline=True)
change_group_keyboard.add(Text("Поменять группу", payload={"cmd": "change group"}), color=KeyboardButtonColor.PRIMARY)

remove_keyboard = Keyboard(one_time=True)


def menu_keyboard():
    menu = Keyboard(one_time=False, inline=False)

    menu.add(Text("🔎 Сегодняшние пары", payload={'cmd': 'today'}), color=KeyboardButtonColor.PRIMARY)
    menu.add(Text("🔎 Завтрашние пары", payload={'cmd': 'tomorrow'}), color=KeyboardButtonColor.PRIMARY)
    menu.row()
    menu.add(Text("Эта неделя", payload={"cmd": "sweek", 'next': False}), color=KeyboardButtonColor.SECONDARY)
    menu.add(Text("Следующая неделя", payload={"cmd": "sweek", 'next': True}), color=KeyboardButtonColor.SECONDARY)
    menu.row()
    menu.add(Text("🛠 Настройки", payload={"cmd": "settings"}), color=KeyboardButtonColor.SECONDARY)
    menu.row()
    menu.add(Text("Убрать клавиатуру", payload={"cmd": "suicide"}), color=KeyboardButtonColor.NEGATIVE)

    return menu
