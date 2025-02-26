import contextlib
from typing import AsyncIterator, TypedDict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

from api.src.controllers.queries import router as queries_router
from api.src.db.config import (
    AsyncSessionMaker,
    create_async_engine,
    create_async_sessionmaker,
)
from api.src.pages.pages import router as pages_router
from api.src.weather.base import BaseWeatherService
from api.src.weather.owm import OWMWeatherService


class State(TypedDict):
    async_engine: AsyncEngine
    async_sessionmaker: AsyncSessionMaker
    weather_service: BaseWeatherService


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    async_engine = create_async_engine()
    async_sessionmaker = create_async_sessionmaker(async_engine)

    yield {
        "async_sessionmaker": async_sessionmaker,
        "weather_service": OWMWeatherService,
    }


app = FastAPI(lifespan=lifespan)

app.include_router(queries_router)
app.include_router(pages_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
