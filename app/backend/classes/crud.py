import ast
import json
from datetime import datetime

import aioredis
from config import settings
from app.backend.base.utils import RedisDatabases
from app.backend.classes.handlers import scrape_spreadsheet
from app.backend.classes.schemas import ClassSchema, DaySchema


class ClassesREDIS:
    def __init__(self):
        # TODO подумать над оптимизацией сессий. Мб контекст для транзакций придумать какой-нибудь

        self.session = aioredis.from_url(
            settings.redis_url + RedisDatabases.CLASSES,
            decode_responses=True
        )

    async def reset_database(self):
        """ Перезаписывает дб с парами на новые. Вызывать раз в час """

        print('обновляю бд')

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
            await client.execute_command('set', 'uptime', str(datetime.now()))

    async def get(self, group_id: int, week_day_index: int, above_line: bool) -> DaySchema | None:
        day_info = {
            'week_day_index': week_day_index,
            'above_line': above_line,
            'group_id': group_id
        }

        async with self.session.client() as client:
            day_classes_raw = await client.execute_command('get', str(day_info))

            if day_classes_raw is None:
                return None

            day_classes_dict = ast.literal_eval(day_classes_raw)
            day_info['classes'] = ast.literal_eval(day_classes_dict.get('classes'))

        classes = []
        for class_raw in day_info.get('classes'):
            string_dictionary = ast.literal_eval(class_raw)
            dictionary_dictionary = ast.literal_eval(string_dictionary)
            classes.append(ClassSchema(**dictionary_dictionary))

        day_info['classes'] = classes
        return DaySchema(**day_info)

    async def get_uptime(self):
        async with self.session.client() as client:
            return await client.execute_command('get', 'uptime')
