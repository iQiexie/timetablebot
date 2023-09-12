from typing import Optional

from sqlalchemy import select, update

from app.backend.core.repo import BaseRepo
from app.backend.db.models.credentials import CredentialsModel


class CredentialsRepo(BaseRepo[CredentialsModel]):
    model = CredentialsModel

    async def create_credentials(self, service_name: str, credentials: str) -> CredentialsModel:
        stmt = select(self.model).where(self.model.service_name == service_name)
        query = await self.session.execute(stmt)
        existing_credential = query.scalar()

        if existing_credential:
            stmt = update(self.model).where(self.model.service_name == service_name).values(credentials=credentials)
            await self.session.execute(stmt)
            existing_credential.credentials = credentials
            return existing_credential

        model = CredentialsModel(service_name=service_name, credentials=credentials)
        self.session.add(model)
        return model

    async def get_credentials(self, service_name: str) -> Optional[CredentialsModel]:
        stmt = select(self.model).where(self.model.service_name == service_name)
        query = await self.session.execute(stmt)
        return query.scalar_one_or_none()
