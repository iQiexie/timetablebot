from sqlalchemy.ext.asyncio import AsyncSession

from refactor.base.crud import BaseCRUD
from refactor.event_logs.models import EventLog
from refactor.event_logs.schemas import EventLogSchema


class EventLogCRUD:
    def __init__(self, db_session: AsyncSession):
        self.model = EventLog
        self.schema = EventLogSchema
        self.base = BaseCRUD(db_session=db_session, model=self.model, schema=self.schema)

    async def create_log(self, **kwargs):
        async with self.base.transaction():
            return await self.base.insert(**kwargs)
