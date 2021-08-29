from vkwave.bots import TextContainsFilter, PayloadFilter

today_filters = (
        (
                TextContainsFilter('бот') & TextContainsFilter('пары') &
                (TextContainsFilter('сёдня') | TextContainsFilter('седня'))
        ) |
        PayloadFilter({"command": "today"})
)

tomorrow_filters = (
        (
                TextContainsFilter('бот') & TextContainsFilter('пары') & TextContainsFilter('завтра')
        ) |
        PayloadFilter({"command": "tomorrow"})
)

start_filters = (
        TextContainsFilter('старт') |
        TextContainsFilter('привет') |
        TextContainsFilter('start') |
        TextContainsFilter('покежь клаву') |
        TextContainsFilter('клава')
)