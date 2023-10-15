from datetime import datetime

from pydantic import BaseModel


class WebAppDateInfo(BaseModel):
    date: datetime
