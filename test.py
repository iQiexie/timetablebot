import asyncio

from refactor.base.db import async_session
from refactor.google_api.crud import GoogleApiCRUD
from refactor.google_api.handlers import GoogleApiHandler


async def test():
    google = GoogleApiHandler(GoogleApiCRUD(async_session))
    await google.init_services()
    await google.update_sheet()
    print(google.drive_service, google.sheets_service)


asyncio.run(test())
