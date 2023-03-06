from aioredis import Redis


class BaseRedis:
    session: Redis

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
