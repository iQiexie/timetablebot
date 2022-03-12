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
from refactor.backend.google_api.handlers import GoogleApiHandler


async def test():
    crud = ClassesREDIS()
    await crud.reset_database()

    res = await crud.get(208, 2, True)

    for re in res:
        print(re)


asyncio.run(test())
