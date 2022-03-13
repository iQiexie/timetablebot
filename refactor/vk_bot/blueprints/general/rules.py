from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from refactor.utils import list_contains_str


class MenuRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'меню',
            'в меню',
            'главное меню',
            'начать',
            'покежь клаву',
            'клава',
            'start',
            'привет',
        ]

        payload = event.payload or 'None'
        if 'main menu' in payload:
            return True

        return list_contains_str(event.text, triggers)
