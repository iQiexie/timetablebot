from sqlalchemy.ext.asyncio import AsyncSession

from refactor.base.crud import BaseCRUD
from refactor.google_api.models import Credential


class GoogleApiCRUD:
    def __init__(self, db_session: AsyncSession):
        self.model = Credential
        self.base = BaseCRUD(db_session=db_session, model=self.model)

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