from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from app.utils import list_contains_str, smart_list_merge
from app.vk_bot.blueprints.utils import check_payload

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
            'завтрашние',
        ]

        payload = await check_payload(event, 'tomorrow')
        triggers = list_contains_str(event.text, smart_list_merge(base_triggers, triggers))

        return payload or triggers


class DaySelectionRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'sweek')


class ByDayRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'by day')


class LegacySearchRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'legacy search')


class LegacySearchBlockRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'show day')


class DownVoteRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'downvote')


class UpVoteRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'upvote')
