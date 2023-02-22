from datetime import datetime
import aioredis
from config import settings


class ClassesREDIS:
    def __init__(self):
        self.session = aioredis.from_url(
            url=f"{settings.REDIS_URL}{settings.REDIS_CLS_DB}",
            decode_responses=True,
            password=settings.REDIS_PASSWORD,
        )

    async def replace_classes(self, classes: dict):
        pipeline = self.session.pipeline()
        pipeline.multi()

        pipeline.flushdb()

        for key, value in classes.items():
            pipeline.set(key, value)

        pipeline.set("last_updated", str(datetime.now()))

        await pipeline.execute()

        await pipeline.reset()

    async def get_partial_match(self, key_pattern: str) -> dict[str, str]:
        pattern = key_pattern + ":*"

        matching_keys = await self.session.keys(pattern)

        if len(matching_keys) == 0:
            return {}

        results = dict()
        for key in matching_keys:
            value = await self.session.get(key)
            results[key] = value

        return results

    async def get(self, key: str) -> str:
        return await self.session.execute_command("get", str(key))
