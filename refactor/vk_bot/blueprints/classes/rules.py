from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from refactor.utils import list_contains_str, smart_list_merge
from refactor.vk_bot.blueprints.utils import check_payload

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
            'сегодняшние',
            'сегодня',
            'сёдня',
            'седня',
            'сейчас',
            'щас',
        ]

        payload = await check_payload(event, 'today')
        triggers = list_contains_str(event.text, smart_list_merge(base_triggers, triggers))

        return payload or triggers


class TomorrowClassesRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'завтра',
        ]

        payload = await check_payload(event, 'tomorrow')
        triggers = list_contains_str(event.text, smart_list_merge(base_triggers, triggers))

        return payload or triggers


class LegacySearchRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'legacy search')
