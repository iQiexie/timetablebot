from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from refactor.vk_bot.blueprints.utils import check_payload


class ChatbotRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return await check_payload(event, 'upvote')
