import asyncio
from contextlib import suppress

# from refactor.classes.crud import ClassesCRUD
# from refactor.classes.handler import test
from refactor.base.db import async_session
from refactor.base.db import Base


async def start():
    # your infinite loop here, for example:
    while True:
        print(Base.metadata)
        await asyncio.sleep(1)


async def main():
    task = asyncio.Task(start())

    # let script some thime to work:
    await asyncio.sleep(70)

    # cancel task to avoid warning:
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task  # await for task cancellation


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
