from app.backend.db.deps import async_session
from app.backend.handlers.classes.main import update_classes
from app.backend.handlers.users.crud import UserCRUD


async def actualize():
    await update_classes()


async def count_users():
    async with async_session() as session:
        await UserCRUD(session=session).record_daily_users()
