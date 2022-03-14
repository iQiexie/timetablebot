import aioredis

from config import settings
from app.backend.base.utils import RedisDatabases


class GoogleApiREDIS:
    def __init__(self):
        self.session = aioredis.from_url(
            settings.redis_url + RedisDatabases.CREDENTIALS,
            decode_responses=True
        )

    async def create(self, service_name: str, credentials: str):
        async with self.session.client() as client:
            ok = await client.execute_command("set", service_name, credentials)
            assert ok is True

    async def get(self, service_name: str):
        async with self.session.client() as client:
            return await client.execute_command("get", service_name)

    async def reset_database(self):
        async with self.session.client() as client:
            await client.execute_command('flushdb')
