from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from app.utils import list_contains_str
from app.vk_bot.blueprints.utils import check_payload


class SettingsRule(ABCRule[BaseMessageMin]):
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


class UptimeRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'uptime')


class ChatBotSettingsRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'update ai')