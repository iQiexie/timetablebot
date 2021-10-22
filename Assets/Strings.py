""" Сообщения """

CHANGE_GROUP_MESSAGE = 'Напиши мне новый номер группы' \
                       '\n\nЕсли вы в беседе, перед номером напишите "бот", например "бот 218"'
INVALID_INPUT_MESSAGE = "Мне нужны только циферки!"
DEFAULT_ANSWER_MESSAGE = 'Oк'
INVALID_COMMAND = 'Я нинаю таких команд((( Попробуй написать "Старт" или "Привет" чтобы открыть меню, ' \
                  'а потом зайти в "Настройки"'


""" Переменные """

current_spreadsheet = {
    "id": None,
    "updated_time": ""
}


""" Кастомные Сообщения """


def Settings(group_index):
    return f"""Твоя/ваша группа: {group_index}

Список команд:
https://vk.com/mpsu_schedule?w=wall-206763355_30
https://vk.com/wall-206763355_42


F.A.Q:
https://vk.com/topic-206763355_48153565

Если чё-то не работает, пиши мне @baboomka"""


def Spreadsheet_update_info():
    return f"Расписание последний раз обновлялось сегодня в {current_spreadsheet['updated_time']}" \
           f"\n\nid: {current_spreadsheet['id']}"
