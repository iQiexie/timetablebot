from vkbottle import Keyboard, Text, KeyboardButtonColor


def get_legacy_search_keyboard(payload: dict):
    """ Payload передавать без cmd """

    payload['cmd'] = 'legacy search'

    legacy_search_keyboard = Keyboard(inline=True)
    legacy_search_keyboard.add(Text("Старый поиск", payload=payload), color=KeyboardButtonColor.PRIMARY)

    return legacy_search_keyboard
