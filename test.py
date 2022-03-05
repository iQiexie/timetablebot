import asyncio

from refactor.classes.crud import ClassesCRUD
from refactor.classes.handler import test
from refactor.base.db import async_session

loop = asyncio.get_event_loop()
loop.run_until_complete(test(ClassesCRUD(async_session)))
loop.close()