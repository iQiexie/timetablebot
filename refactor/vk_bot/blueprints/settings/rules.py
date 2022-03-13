from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from refactor.utils import list_contains_str


class GeneralRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'настройки',
            'settings',
        ]

        return list_contains_str(event.text, triggers)


class ChangeGroupRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'поменять группу',
            'выбрать группу',
            'сменить группу',
        ]

        payload = event.payload or 'None'

        if 'change group' in payload:
            return True
        elif list_contains_str(event.text, triggers):
            return True
