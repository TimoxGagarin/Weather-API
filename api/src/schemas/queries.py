from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.src.schemas.base import Pagination


class DisplayQuery(BaseModel):
    id: UUID
    city: str
    temp: float
    wind_speed: float
    wind_degree: int
    humidity: int
    description: str
    pressure: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateQuery(BaseModel):
    city: str


class SearchQuery(Pagination):
    city: str | None = None
