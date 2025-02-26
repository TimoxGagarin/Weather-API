from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as GUID
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def to_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if "_sa_" != k[:4]}

    def __repr__(self):
        return f"""<{self.__class__.__name__}({
            [
                ", ".join(
                    "%s=%s" % (k, self.__dict__[k])
                    for k in self.__dict__
                    if "_sa_" != k[:4]
                )
            ]
        }"""


class Queries(Base):
    __tablename__ = "queries"

    id: Mapped[UUID] = mapped_column(GUID, primary_key=True, default=uuid4)
    city: Mapped[str] = mapped_column(String(length=320), index=True, nullable=False)
    temp: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    wind_degree: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(
        String(length=320), index=True, nullable=False
    )
    rain: Mapped[str] = mapped_column(String(length=320), nullable=True)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
    pressure: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
