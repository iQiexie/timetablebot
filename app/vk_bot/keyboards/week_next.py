from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor
from vkbottle import Text

next_week_keyboard = Keyboard(inline=False, one_time=False)


next_week_keyboard.add(
    Text('Понедельник', payload={'cmd': 'by day', 'next': True, 'day': 1}),
    color=KeyboardButtonColor.SECONDARY
)

next_week_keyboard.add(
    Text('Вторник', payload={'cmd': 'by day', 'next': True, 'day': 2}),
    color=KeyboardButtonColor.SECONDARY
)

next_week_keyboard.row()

next_week_keyboard.add(
    Text('Среда', payload={'cmd': 'by day', 'next': True, 'day': 3}),
    color=KeyboardButtonColor.SECONDARY
)

next_week_keyboard.add(
    Text('Четверг', payload={'cmd': 'by day', 'next': True, 'day': 4}),
    color=KeyboardButtonColor.SECONDARY
)

next_week_keyboard.row()

next_week_keyboard.add(
    Text('Пятница', payload={'cmd': 'by day', 'next': True, 'day': 5}),
    color=KeyboardButtonColor.SECONDARY
)

next_week_keyboard.add(
    Text('Суббота', payload={'cmd': 'by day', 'next': True, 'day': 6}),
    color=KeyboardButtonColor.SECONDARY
)

next_week_keyboard.row()

next_week_keyboard.add(Text("В меню", payload={"cmd": "main menu"}), color=KeyboardButtonColor.NEGATIVE)
