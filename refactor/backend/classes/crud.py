import ast
import json
from typing import List

import aioredis
from config import settings
from refactor.backend.base.utils import RedisDatabases
from refactor.backend.classes.handlers import scrape_spreadsheet
from refactor.backend.classes.schemas import ClassSchema, DaySchema


class ClassesREDIS:
    def __init__(self):
        # TODO подумать над оптимизацией сессий. Мб контекст для транзакций придумать какой-нибудь

        self.session = aioredis.from_url(
            settings.redis_url + RedisDatabases.CLASSES,
            decode_responses=True
        )

    async def reset_database(self):
        """ Перезаписывает дб с парами на новые. Вызывать раз в час """

        # TODO либо придумать чё-нибудь с этим, либо короче высылать юзверу сообщение о том, что бд обновляется \
        # TODO если запрос придёт в это время
        # как вариант, можно не флашить дб, а поочерёдно удалять листы, когда обновляешь дб.
        # но тогда надо из scrape_spreadhseet возвращать пары не просто одним большим списком, а по дням
        # потому что по сути, один редис лист - один день

        day_schemas = await scrape_spreadsheet()

        for day_schema in day_schemas:
            await self._insert(day_schema)

    async def _insert(self, day: DaySchema):
        """ Кладёт пару в лист редиса. Проверяет на бубликаты """

        key = {
            'week_day_index': day.week_day_index,
            'above_line': day.above_line,
            'group_id': day.group_id
        }

        value = {
            'classes': str([json.dumps(str(class_model.dict())) for class_model in day.classes])
        }

        async with self.session.client() as client:
            exists = await client.execute_command('exists', str(key))
            if exists:
                await client.execute_command('del', str(key))

            await client.execute_command('set', str(key), str(value))

    async def get(self, group_id: int, week_day_index: int, above_line: bool) -> DaySchema:
        day_info = {
            'week_day_index': week_day_index,
            'above_line': above_line,
            'group_id': group_id
        }

        async with self.session.client() as client:
            day_classes_raw = await client.execute_command('get', str(day_info))
            day_classes_dict = ast.literal_eval(day_classes_raw)
            day_info['classes'] = ast.literal_eval(day_classes_dict.get('classes'))

        classes = []
        for class_raw in day_info.get('classes'):
            string_dictionary = ast.literal_eval(class_raw)
            dictionary_dictionary = ast.literal_eval(string_dictionary)
            classes.append(ClassSchema(**dictionary_dictionary))

        day_info['classes'] = classes
        return DaySchema(**day_info)
