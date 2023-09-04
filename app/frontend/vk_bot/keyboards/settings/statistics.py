from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor
from vkbottle import Text

statistics_keyboard = Keyboard(one_time=False, inline=False)
statistics_keyboard.add(
    Text("👥‍ За последние сутки", payload={"cmd": "usercount"}),
    color=KeyboardButtonColor.PRIMARY,
)
statistics_keyboard.add(
    Text("📆 По дням", payload={"cmd": "daily_usercount"}),
    color=KeyboardButtonColor.PRIMARY,
)
statistics_keyboard.row()
statistics_keyboard.add(
    Text("🏫 По курсам", payload={"cmd": "grade_usercount"}),
    color=KeyboardButtonColor.PRIMARY,
)
statistics_keyboard.add(
    Text("🎓 По Группам", payload={"cmd": "group_usercount"}),
    color=KeyboardButtonColor.PRIMARY,
)
statistics_keyboard.row()
statistics_keyboard.add(
    Text("В настройки", payload={"cmd": "settings"}),
    color=KeyboardButtonColor.NEGATIVE,
)
statistics_keyboard.add(
    Text("В меню", payload={"cmd": "main menu"}),
    color=KeyboardButtonColor.NEGATIVE,
)
