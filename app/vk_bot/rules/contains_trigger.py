from typing import List
from typing import Optional

from vkbottle import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin


class ContainsTriggerRule(ABCRule[BaseMessageMin]):
    def __init__(
        self,
        triggers: Optional[List[str]] = None,
        payload_triggers: Optional[List[str]] = None,
    ):
        if not triggers and not payload_triggers:
            raise AttributeError("Specify triggers or/and payload_triggers")

        self.triggers = triggers or []
        self.payload_triggers = payload_triggers or []

    async def check(self, event: BaseMessageMin) -> bool:
        for trigger in self.triggers:
            if trigger in event.text.lower():
                return True

        payload = event.payload or "None"
        for payload_trigger in self.payload_triggers:
            if payload_trigger in payload:
                return True
