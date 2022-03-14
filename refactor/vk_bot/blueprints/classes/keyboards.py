from vkbottle import Keyboard, Text, KeyboardButtonColor


def class_keyboard(payload: dict):
    """ Payload передавать без cmd """

    legacy = {'cmd': 'legacy search', **payload}
    upvote = {'cmd': 'upvote', **payload}
    downvote = {'cmd': 'downvote', **payload}


    legacy_search_keyboard = Keyboard(inline=True)
    legacy_search_keyboard.add(Text("👍 Правильно", payload=upvote), color=KeyboardButtonColor.POSITIVE)
    legacy_search_keyboard.add(Text("🔎 Старый поиск", payload=legacy), color=KeyboardButtonColor.PRIMARY)
    legacy_search_keyboard.add(Text("👎 Неправильно", payload=downvote), color=KeyboardButtonColor.NEGATIVE)

    return legacy_search_keyboard
