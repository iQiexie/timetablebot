# ... Сообщения ...
__TROUBLESHOOT = 'Если не получается поменять группу, попробуй написать "Старт" чтобы открыть меню, ' \
               'а потом зайти в "Настройки"'
__COMMANDS_LIST = 'vk.com/@mpsu_schedule-vse-komandy-bota'

DEFAULT_ANSWER_MESSAGE = 'Oк'

GREETINGS = 'Привет! Для начала работы с ботом тебе нужно написать "Старт" или "Начать", ' \
            'а потом тебе нужно поменять свою группу через настройки.' \
            '\n\nСписок команд:' \
            '\n' + __COMMANDS_LIST

CHANGE_GROUP_MESSAGE = 'Напиши мне новый номер группы' \
                       '\n\nЕсли вы в беседе, перед номером напишите "бот", например "бот 218"'
INVALID_INPUT_MESSAGE = "Мне нужны только циферки!"

INVALID_COMMAND = 'Если ты пытаешься со мной поболтать, то не получится(' \
                  '\nМой интеллект теперь включается только по команде.' \
                  '\n\nНапиши "Старт", потом нажми на "Настройки" и после нажми на "Виртуальный собеседник: Выкл"' \
                  '\n\n Список команд:' \
                  '\n' + __COMMANDS_LIST \
                  + '\n\n' + __TROUBLESHOOT

WRONG_COMMUNITY = 'Если ты пытаешься со мной поболтать, то в этой группе у тебя не получится :(' \
                  '\nМне отключили интеллект, потому что я "слишком грубый" 😢' \
                  '\n\nЕсли хочешь поболтать, я свободен в группе:' \
                  '\nhttps://vk.com/mpsu_schedule' \
                  '\n\nЧто-то не работает?' \
                  '\n' + __TROUBLESHOOT

# ... Переменные ...

current_spreadsheet = {
    "id": None,
    "updated_time": ""
}

AI_FRIEND = "Виртуальный собеседник "


# ... Кастомные сообщения ...


def Settings(group_index):
    return f"""Твоя/ваша группа: {group_index}

Список команд:
{__COMMANDS_LIST}

F.A.Q:
https://vk.com/topic-206763355_48153565

Если чё-то не работает, пиши мне @baboomka"""


def Spreadsheet_update_info():
    return f"Расписание последний раз обновлялось сегодня в {current_spreadsheet['updated_time']}" \
           f"\n\nid: {current_spreadsheet['id']}"
