# import asyncio
# from contextlib import suppress
#
# from refactor.classes.crud import ClassesCRUD
# from refactor.classes.handlers import test
# from refactor.base.db import async_session
#
#
# async def start():
#     # your infinite loop here, for example:
#     while True:
#         print(await test(ClassesCRUD(async_session)))
#         await asyncio.sleep(1)
#
#
# async def main():
#     task = asyncio.Task(start())
#
#     # let script some thime to work:
#     await asyncio.sleep(1)
#
#     # cancel task to avoid warning:
#     task.cancel()
#     with suppress(asyncio.CancelledError):
#         await task  # await for task cancellation
#
#
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.run_until_complete(loop.shutdown_asyncgens())
#     loop.close()
from refactor.google_api.handlers import Create_Service
from config import settings

sheets_service = Create_Service(
    settings.google_secret,
    'sheets',
    'v4',
    ['https://www.googleapis.com/auth/spreadsheets.readonly']
)

