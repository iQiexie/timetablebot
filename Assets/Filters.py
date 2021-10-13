from vkwave.bots import TextContainsFilter, PayloadFilter


def group_message(peer_id, message) -> bool:
    # если сообщение из беседы

    return (message.lower().startswith('бот ') | message.lower().startswith('[club')) and int(peer_id) > 2000000000


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
        TextContainsFilter('эта неделя') |
        PayloadFilter({"command": "this week"})
)

next_week = (
        (TextContainsFilter('след неделя') | TextContainsFilter('следующая неделя')) |
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

last_update_time = (
        TextContainsFilter('актуальность') |
        TextContainsFilter('расписания') |
        TextContainsFilter('обновился') |
        TextContainsFilter('uptime') |
        TextContainsFilter('аптайм') |
        (TextContainsFilter('время') & TextContainsFilter('обновления')) |
        (TextContainsFilter('время') & TextContainsFilter('обновы')) |
        PayloadFilter({"command": "get spreadsheet uptime"})
)
