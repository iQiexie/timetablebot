from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from refactor.utils import list_contains_str

base_triggers = [
    'пары',
    'расписание',
    'занятия',
    'уроки',
    'список',
]


class TodayClassesRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'сегодня',
            'сёдня',
            'седня',
            'сейчас',
            'щас',
        ]

        return list_contains_str(event.text, triggers + base_triggers)


class TomorrowClassesRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'завтра',
        ]

        return list_contains_str(event.text, triggers + base_triggers)
