import collections

import aioredis

from app.backend.redis.base_redis import BaseRedis
from config import settings


class ChatGptREDIS(BaseRedis):
    def __init__(self):
        self.session = aioredis.from_url(
            url=f"{settings.REDIS_URL}{settings.REDIS_GTP_DB}",
            decode_responses=True,
            password=settings.REDIS_PASSWORD,
        )

    async def append_message(self, vk_id: int, message: str, role: str):
        last_index_key = f"{vk_id}:LAST_INDEX"
        last_index = await self.session.get(last_index_key) or 0

        pipeline = self.session.pipeline()
        pipeline.multi()

        key = f"{vk_id}:INDEX:{last_index}:{role}"
        await pipeline.set(key, str(message))
        await pipeline.set(last_index_key, int(last_index) + 1)
        await pipeline.execute()
        await pipeline.reset()

    async def get_history(self, vk_id: int):
        r = await self.get_partial_match(key_pattern=f"{vk_id}:INDEX")
        od = collections.OrderedDict(sorted(r.items()))
        return od

    async def delete_history(self, vk_id: int):
        keys = await self.session.keys(f"{vk_id}:*")
        if keys:
            await self.session.delete(*keys)
