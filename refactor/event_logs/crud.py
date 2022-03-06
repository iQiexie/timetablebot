import enum
from sqlalchemy.ext.asyncio import AsyncSession
from refactor.base.crud import BaseCRUD
from refactor.event_logs.models import EventLog, EventLogType, EventLogAction
from refactor.event_logs.schemas import EventLogSchema


class EventLogActionMixin:
    def __init__(self, type_verbose, crud: BaseCRUD):
        self._type_verbose: enum = type_verbose
        self.crud = crud

    async def spreadsheet(self, data: str = None):
        if not data:
            data = "spreadsheet operation"

        async with self.crud.transaction():
            await self.crud.insert(
                data=data,
                event_type=self._type_verbose,
                event_action=EventLogAction.SPREADSHEET
            )

    async def lesson(self, user_id):
        async with self.crud.transaction():
            await self.crud.insert(
                user_id=user_id,
                data="class operation",
                event_type=self._type_verbose,
                event_action=EventLogAction.CLASS
            )


class EventLogTypeMixin:
    def __init__(self, crud: BaseCRUD):
        self.read = EventLogActionMixin(EventLogType.READ, crud)
        self.created = EventLogActionMixin(EventLogType.CREATE, crud)
        self.updated = EventLogActionMixin(EventLogType.UPDATE, crud)
        self.deleted = EventLogActionMixin(EventLogType.DELETE, crud)


class EventLogCRUD:
    def __init__(self, db_session: AsyncSession):
        self._model = EventLog
        self._schema = EventLogSchema
        self._base = BaseCRUD(db_session=db_session, model=self._model, schema=self._schema)
        self.new_log = EventLogTypeMixin(self._base)

