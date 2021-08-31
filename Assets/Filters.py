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

start_filters_dm = (
        TextContainsFilter('старт') |
        TextContainsFilter('привет') |
        TextContainsFilter('start') |
        TextContainsFilter('начать') |
        TextContainsFilter('покежь клаву') |
        TextContainsFilter('клава')
)

start_filters_group = (
        TextContainsFilter('бот старт') |
        TextContainsFilter('бот привет') |
        TextContainsFilter('бот start') |
        TextContainsFilter('бот начать') |
        TextContainsFilter('бот покежь клаву') |
        TextContainsFilter('бот клава')
)