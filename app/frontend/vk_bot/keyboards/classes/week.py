from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor
from vkbottle import Text


def compose_detailed_menu(pattern: str = None) -> Keyboard:
    keyboard = Keyboard(one_time=False, inline=False)

    keyboard.add(
        Text("👈 Эта неделя", {"cmd": "sweek", "next": False, "match": pattern}),
        KeyboardButtonColor.SECONDARY,
    )
    keyboard.add(
        Text("👉 Следующая неделя", {"cmd": "sweek", "next": True, "match": pattern}),
        KeyboardButtonColor.SECONDARY,
    )

    if pattern:
        keyboard.row()
        keyboard.add(Text("⚠️ Режим поиска по шаблону", {"cmd": "searching_status"}))

    else:
        keyboard.row()
        keyboard.add(
            Text("👩‍🏫 Поиск по преподавателю", {"cmd": "pattern_search"}),
            KeyboardButtonColor.SECONDARY,
        )

    keyboard.row()
    keyboard.add(
        Text("В меню", payload={"cmd": "main menu"}),
        color=KeyboardButtonColor.NEGATIVE,
    )

    return keyboard


def compose_week_keyboard(next_week: bool, pattern: str = None) -> Keyboard:
    keyboard = Keyboard(inline=False, one_time=False)

    payload = {
        "cmd": "by day",
        "next": next_week,
    }

    if pattern:
        payload["match"] = pattern

    keyboard.add(
        Text("Понедельник", payload=dict(day=1, **payload)),
        color=KeyboardButtonColor.SECONDARY,
    )

    keyboard.add(
        Text("Вторник", payload=dict(day=2, **payload)),
        color=KeyboardButtonColor.SECONDARY,
    )

    keyboard.row()

    keyboard.add(
        Text("Среда", payload=dict(day=3, **payload)),
        color=KeyboardButtonColor.SECONDARY,
    )

    keyboard.add(
        Text("Четверг", payload=dict(day=4, **payload)),
        color=KeyboardButtonColor.SECONDARY,
    )

    keyboard.row()

    keyboard.add(
        Text("Пятница", payload=dict(day=5, **payload)),
        color=KeyboardButtonColor.SECONDARY,
    )

    keyboard.add(
        Text("Суббота", payload=dict(day=6, **payload)),
        color=KeyboardButtonColor.SECONDARY,
    )

    keyboard.row()

    keyboard.add(
        Text("Назад", payload={"cmd": "detailed", "match": pattern}),
        color=KeyboardButtonColor.NEGATIVE,
    )

    keyboard.add(Text("В меню", payload={"cmd": "main menu"}), color=KeyboardButtonColor.NEGATIVE)

    return keyboard


reset_keyboard = Keyboard(inline=True)
reset_keyboard.add(
    Text("Сбросить режим поиска по шаблону", payload={"cmd": "detailed"}),
    color=KeyboardButtonColor.NEGATIVE,
)
