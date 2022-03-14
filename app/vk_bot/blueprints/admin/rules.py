from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from app.utils import list_contains_str


class UpdateClassesDbRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        triggers = [
            'обнови пары'
        ]

        return list_contains_str(event.text, triggers)
