import ast
import json
from typing import List

import aioredis
from config import settings
from refactor.backend.classes.schemas import ClassSchema


class ClassesREDIS:
    def __init__(self):
        # TODO подумать над оптимизацией сессий. Мб контекст для транзакций придумать какой-нибудь

        self.session = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            decode_responses=True
        )

    async def insert(self, class_object: ClassSchema):
        key = {
            'week_day_index': class_object.week_day_index,
            'above_line': class_object.above_line,
            'group_id': class_object.group_id
        }

        value = {
            'index': class_object.index,
            'text': class_object.text,
            'hyperlinks': class_object.hyperlinks,
        }

        exists = await self.session.lpos(str(key), str(value))
        list_length = await self.session.llen(str(key))

        if isinstance(exists, int):
            return

        if list_length >= settings.CLASSES_PER_DAY:
            await self.session.delete(str(key))

        await self.session.rpush(str(key), str(value))

    async def get(self, group_id: int, week_day_index: int, above_line: bool) -> List[ClassSchema]:
        key = {
            'week_day_index': week_day_index,
            'above_line': above_line,
            'group_id': group_id
        }

        list_length = await self.session.llen(str(key))
        results = await self.session.lrange(str(key), 0, list_length)
        classes = []

        for result in results:
            result_dict = ast.literal_eval(result)

            class_object = ClassSchema(
                week_day_index=week_day_index,
                above_line=above_line,
                group_id=group_id,
                index=result_dict.get('index'),
                text=result_dict.get('text'),
                hyperlinks=result_dict.get("hyperlinks")
            )
            classes.append(class_object)

        return classes
