from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from refactor.utils import list_contains_str


class SettingsGeneralRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'настройки',
        ]

        return list_contains_str(event.text, triggers)
