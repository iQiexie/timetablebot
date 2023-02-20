from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class NoBotMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        if self.event.peer_id < 2000000000:
            return

        text_mention = self.event.text.lower().startswith("бот ")
        mention_mention = self.event.mention.text.startswith("@")
        if not any([text_mention, mention_mention]):
            print("Получено групповое сообщение, не относящееся к боту")
            self.stop()
