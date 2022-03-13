from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from refactor.utils import list_contains_str


class HelloRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'привет',
            'начать',
            'start',
            'начать',
            'покежь клаву',
            'клава',
        ]

        return list_contains_str(event.text, triggers)
