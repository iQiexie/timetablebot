from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from app.backend.db.deps import async_session
from app.backend.handlers.users.crud import UserCRUD
from app.backend.handlers.users.schemes import UserSchema
from app.vk_bot.error_handlers import error_handler


class AuthMiddleware(BaseMiddleware[Message]):
    @error_handler.catch
    async def pre(self) -> None:
        async with async_session() as session:
            users = UserCRUD(session=session)
            user = await users.get(self.event.peer_id)

            if user is None:
                user = await users.create(vk_id=self.event.peer_id)

        await users.mark_last_activity(vk_id=self.event.peer_id)
        self.send({"user": UserSchema.from_orm(user)})
