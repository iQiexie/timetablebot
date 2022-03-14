from vkbottle.tools.dev.mini_types.base import BaseMessageMin


async def check_payload(event: BaseMessageMin, key: str) -> bool:
    payload = event.payload or 'None'
    if key in payload:
        return True
