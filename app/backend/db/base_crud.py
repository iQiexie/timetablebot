from typing import Generic
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db.base_model import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(Generic[ModelType]):
    def __init__(self, session: AsyncSession):
        self.session = session
