from sqlalchemy import Column, Integer, String
from refactor.backend.base.db import Base, TimestampMixin


class Credential(Base, TimestampMixin):
    __tablename__ = "google_credentials"

    id = Column(Integer, primary_key=True, index=True)

    service_name = Column(String(255), unique=True)
    credentials = Column(String(1000), unique=True)
