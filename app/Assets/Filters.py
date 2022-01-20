import json

from vkwave.bots import TextContainsFilter, PayloadFilter, BaseEvent
from vkwave.bots.core.dispatching.filters.base import FilterResult, BaseFilter
from vkwave.bots.core.dispatching.filters.builtin import get_payload
from vkwave.bots.core.types.json_types import JSONDecoder


def group_message(peer_id, message) -> bool:
    # если сообщение из беседы

    return (message.lower().startswith('бот ') | message.lower().startswith('[club')) and int(peer_id) > 2000000000


def dm_message(peer_id) -> bool:
    return int(peer_id) < 2000000000


# Фильтры today, tomorrow дублируются в Catchup.py

today = ((
                 (TextContainsFilter('пары') | TextContainsFilter('список') | TextContainsFilter('Расписание')) &
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

update_ai = (
        PayloadFilter({"command": "update ai"})
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
        TextContainsFilter('start') |
        TextContainsFilter('начать') |
        TextContainsFilter('покежь клаву') |
        TextContainsFilter('клава')
)

last_update_time = (
        TextContainsFilter('актуальность') |
        TextContainsFilter('обновился') |
        TextContainsFilter('uptime') |
        TextContainsFilter('аптайм') |
        (TextContainsFilter('время') & TextContainsFilter('обновления')) |
        (TextContainsFilter('время') & TextContainsFilter('обновы')) |
        PayloadFilter({"command": "get spreadsheet uptime"})
)


class CustomPayloadContainsFilter(BaseFilter):
    """
        Checking payload dict contains some key
    """

    def __init__(self, key: str, json_loader: JSONDecoder = json.loads):
        self.key = key
        self.json_loader = json_loader

    async def check(
        self,
        event: BaseEvent,
    ) -> FilterResult:
        current_payload = get_payload(event)
        if current_payload is None:
            return FilterResult(False)
        return FilterResult(self.key in str(current_payload))
