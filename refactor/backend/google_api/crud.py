from sqlalchemy.ext.asyncio import AsyncSession

from refactor.backend.base.crud import BaseCRUD
from refactor.backend.event_logs.crud import EventLogCRUD
from refactor.backend.google_api.models import Credential
from refactor.backend.google_api.schemas import CredentialSchema


# TODO перенести на редис


class GoogleApiCRUD:
    def __init__(self, db_session: AsyncSession):
        self.model = Credential
        self.schema = CredentialSchema
        self.base = BaseCRUD(db_session=db_session, model=self.model, schema=self.schema)

        self.logger = EventLogCRUD(db_session=db_session)

    async def create(self, **kwargs):
        async with self.base.transaction():
            return await self.base.insert(**kwargs)

    async def get(self, service_name: str):
        async with self.base.transaction():
            return await self.base.get_one(self.model.service_name == service_name)

    async def update(self, service_name: str, **kwargs):
        async with self.base.transaction():
            return await self.base.update(self.model.service_name == service_name, **kwargs)

    async def delete(self, service_name: str):
        async with self.base.transaction():
            return await self.base.delete(self.model.service_name == service_name)
