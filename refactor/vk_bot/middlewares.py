from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from refactor.vk_bot.states import PickingState
from refactor.vk_bot.storages import context_storage


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


middlewares = [GroupPickingMiddleware]
