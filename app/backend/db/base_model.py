from typing import TypeVar
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

metadata = MetaData()
Base = declarative_base(metadata=metadata)

BaseModelType = TypeVar("BaseModelType", bound=Base)
