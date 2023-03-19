from datetime import datetime
import aioredis

from app.backend.redis.base_redis import BaseRedis
from config import settings


class ClassesREDIS(BaseRedis):
    def __init__(self):
        self.session = aioredis.from_url(
            url=f"{settings.REDIS_URL}{settings.REDIS_CLS_DB}",
            decode_responses=True,
            password=settings.REDIS_PASSWORD,
        )

    async def replace_classes(self, classes: dict):
        pipeline = self.session.pipeline()
        pipeline.multi()

        await pipeline.flushdb()

        for key, value in classes.items():
            await pipeline.set(key, value)

        await pipeline.set("last_updated", str(datetime.now()))

        await pipeline.execute()

        await pipeline.reset()

    async def get(self, key: str) -> str:
        return await self.session.execute_command("get", str(key))

    async def get_by_value(self, pattern: str) -> dict[str, str]:
        key_value_pairs = dict()

        keys = await self.session.keys(pattern="*")
        values = await self.session.mget(keys=[*keys])
        for key, value in zip(keys, values):
            if pattern.casefold() in value.casefold():
                key_value_pairs[key] = value

        return key_value_pairs
