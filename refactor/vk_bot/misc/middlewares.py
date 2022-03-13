from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from refactor.backend.base.db import async_session
from refactor.backend.users.crud import UserCRUD
from refactor.vk_bot.misc.states import PickingState
from refactor.vk_bot.misc.storages import context_storage

db = UserCRUD(async_session)


class AuthMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:

        user = await db.get(self.event.peer_id)

        if user is None:
            await db.create(vk_id=self.event.peer_id)

        user = await db.get(vk_id=self.event.peer_id)

        self.send({'user': user})

class GroupPickingMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:
        state = self.event.state_peer
        if state is None:
            return

        if state.state == f"PickingState:{PickingState.PICKING_GROUP}":
            if not self.event.text.isdigit():
                await self.event.answer(state.payload.get('error'))
                print(f"{self.event.peer_id} is picking group and entered {self.event.text}")
                self.stop()


middlewares = [GroupPickingMiddleware, AuthMiddleware]
