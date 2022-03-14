from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from app.utils import list_contains_str
from app.vk_bot.blueprints.utils import check_payload


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
            'старт',
            'привет',
        ]

        payload = event.payload or 'None'
        if 'main menu' in payload:
            return True

        return list_contains_str(event.text, triggers)


class KillKeyboardRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'suicide')
