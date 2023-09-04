from sqlalchemy import Column
from sqlalchemy import String

from app.backend.db.base_model import Base
from app.backend.db.mixins import TimeMixin


class CredentialsModel(TimeMixin, Base):
    __tablename__ = "credentials"

    service_name = Column(String, primary_key=True, index=True)
    credentials = Column(String)
