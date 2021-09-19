from vkwave.bots import TextContainsFilter, PayloadFilter


def group_message(peer_id, message) -> bool:
    # если сообщение из беседы

    return message.startswith('бот ') and int(peer_id) > 2000000000


def dm_message(peer_id) -> bool:
    return int(peer_id) < 2000000000


today = ((
                 TextContainsFilter('пары') &
                 (TextContainsFilter('сёдня') | TextContainsFilter('седня') | TextContainsFilter('сегодня'))
         ) |
         PayloadFilter({"command": "today"})
         )

tomorrow = (
        (TextContainsFilter('пары') & TextContainsFilter('завтра')) |
        PayloadFilter({"command": "tomorrow"})
)

settings = (
        TextContainsFilter('настройки') |
        PayloadFilter({"command": "settings"})
)

change_group = (
        TextContainsFilter('поменять группу') |
        PayloadFilter({"command": "change group"})
)

this_week = (
        TextContainsFilter('покежь эту неделю') |
        PayloadFilter({"command": "this week"})
)

next_week = (
        (TextContainsFilter('покежь след неделю') | TextContainsFilter('покежь следующую неделю')) |
        PayloadFilter({"command": "next week"})
)

kill_keyboard = (
        TextContainsFilter('убрать клаву') |
        PayloadFilter({"command": "kill keyboard"})
)

main_menu = (
        TextContainsFilter('меню') |
        TextContainsFilter('в меню') |
        TextContainsFilter('главное меню') |
        PayloadFilter({"command": "kill keyboard"})
)


start = (
        TextContainsFilter('старт') |
        TextContainsFilter('привет') |
        TextContainsFilter('start') |
        TextContainsFilter('начать') |
        TextContainsFilter('покежь клаву') |
        TextContainsFilter('клава')
)
