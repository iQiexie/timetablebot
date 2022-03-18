from vkbottle import Keyboard, Text, KeyboardButtonColor


def class_keyboard(payload: dict):
    """ Payload передавать без cmd """

    legacy = {'cmd': 'legacy search', **payload}
    upvote = {'cmd': 'upvote', **payload}
    downvote = {'cmd': 'downvote', **payload}

    legacy_search_keyboard = Keyboard(inline=True)
    legacy_search_keyboard.add(Text("👍 Правильно", payload=upvote), color=KeyboardButtonColor.POSITIVE)
    # legacy_search_keyboard.add(Text("🔎 Старый поиск", payload=legacy), color=KeyboardButtonColor.PRIMARY)
    legacy_search_keyboard.add(Text("👎 Неправильно", payload=downvote), color=KeyboardButtonColor.NEGATIVE)

    return legacy_search_keyboard


def by_day_keyboard(next_week: bool = False):
    keyboard = Keyboard(inline=False, one_time=False)

    keyboard.add(
        Text('Понедельник', payload={'cmd': 'by day', 'next': next_week, 'day': 0}),
        color=KeyboardButtonColor.SECONDARY
    )

    keyboard.add(
        Text('Вторник', payload={'cmd': 'by day', 'next': next_week, 'day': 1}),
        color=KeyboardButtonColor.SECONDARY
    )

    keyboard.row()

    keyboard.add(
        Text('Среда', payload={'cmd': 'by day', 'next': next_week, 'day': 2}),
        color=KeyboardButtonColor.SECONDARY
    )

    keyboard.add(
        Text('Четверг', payload={'cmd': 'by day', 'next': next_week, 'day': 3}),
        color=KeyboardButtonColor.SECONDARY
    )

    keyboard.row()

    keyboard.add(
        Text('Пятница', payload={'cmd': 'by day', 'next': next_week, 'day': 4}),
        color=KeyboardButtonColor.SECONDARY
    )

    keyboard.add(
        Text('Суббота', payload={'cmd': 'by day', 'next': next_week, 'day': 5}),
        color=KeyboardButtonColor.SECONDARY
    )

    keyboard.row()

    keyboard.add(Text("В меню", payload={"cmd": "main menu"}), color=KeyboardButtonColor.NEGATIVE)

    return keyboard
