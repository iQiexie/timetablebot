import asyncio
import aioredis
import json
import ast

from config import settings
from refactor.backend.base.db import async_session
from refactor.backend.classes.crud import ClassesREDIS
from refactor.backend.classes.handlers import scrape_spreadsheet


# async def test():
#     db = ClassesCRUD(async_session)
#     results = await scrape_spreadsheet()
#     # await db.empty_table()
#     for res in results:
#         await db.create(**res.dict())
#     res = await db.get(208, 2, False)
#     for r in res:
#         print(r)
from refactor.backend.classes.schemas import ClassSchema


async def test():
    crud = ClassesREDIS()
    # results = await scrape_spreadsheet()
    #
    # for result in results:
    #     await crud.insert(result)

    res = await crud.get(208, 2, True)

    for re in res:
        print(re)

    #####################################
    #
    # for i in range(3):
    #     string = f"value {i}"
    #     exists = await redis_client.lpos("kek list", string)
    #
    #     if not isinstance(exists, int):
    #         await redis_client.rpush("kek list", string)
    #
    # llen = await redis_client.llen("kek list")
    # values = await redis_client.lrange("kek list", 0, llen)
    # print(values)

    # _class1 = {
    #     'week_day_index': 7,
    #     'above_line': True,
    #     'group_id': 218
    # }
    #
    # _class2 = {
    #     'week_day_index': 3,
    #     'above_line': False,
    #     'group_id': 218
    # }
    #
    # _class3 = {
    #     'week_day_index': 66,
    #     'above_line': False,
    #     'group_id': 333
    # }
    #
    # dict1 = {'cool dict': 'lol', 'hyperlinks': 'rickrooll.com'}
    # dict2 = {'cool dict': 'lol2', 'hyperlinks': 'gggegergegr.com'}
    # dict3 = {'cool dict': 'lol32', 'hyperlinks': 'vvvvvvvvzzzzzzzz.com'}
    #
    # await redis_client.append(str(_class3), f"; {dict1};")
    # await redis_client.append(str(_class3), f"; {dict2};")
    # await redis_client.append(str(_class3), f"; {dict3};")
    #
    # res1 = await redis_client.get(str(_class3))
    # res1 = res1.replace('; ', '').split(';')
    #
    #
    # for i in res1:
    #     print(i)
    # print(json.loads(json.dumps(res1)))
    # print(json.loads(json.dumps(res2)))
    # print(json.loads(res2))


asyncio.run(test())
