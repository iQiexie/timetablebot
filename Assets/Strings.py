CHANGE_GROUP_MESSAGE = "Напишите мне новый номер группы"
INVALID_INPUT_MESSAGE = "Мне нужны только циферки!"
DEFAULT_ANSWER_MESSAGE = 'Oк'
INVALID_COMMAND = 'Я нинаю таких команд((( Попробуй написать "Старт" или "Привет" чтобы открыть меню,' \
                  'а потом зайти в "Настройки"'


def Settings(group_index):
    return f"""Ваша группа: {group_index}

Список команд:
https://vk.com/mpsu_schedule?w=wall-206763355_30

Если чё-то не работает, пиши мне @baboomka
F.A.Q https://vk.com/topic-206763355_48153565"""
