import logging

from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from app.frontend.vk_bot.misc.constants import GROUPS_STARTING_ID


class NoBotMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:
        if self.event.peer_id < GROUPS_STARTING_ID:
            return

        text_mention = self.event.text.lower().startswith("бот ")
        mention_mention = self.event.mention.text.startswith("@")
        if not any([text_mention, mention_mention]):
            logging.info("Получено групповое сообщение, не относящееся к боту")
            self.stop()
