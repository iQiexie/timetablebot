from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from app.frontend.clients.request_clients import RequestClients
from app.frontend.common.dto.user import CreateUser
from app.frontend.vk_bot.misc.error_handlers import error_handler


class AuthMiddleware(BaseMiddleware[Message]):
    @error_handler.catch
    async def pre(self) -> None:
        vk_user = await self.event.get_user()
        user = await RequestClients.vk_backend.get_user(
            data=CreateUser(
                vk_id=self.event.peer_id,
                first_name=vk_user.first_name,
                last_name=vk_user.last_name,
                username=vk_user.domain,
            )
        )
        self.send({"user": user})
