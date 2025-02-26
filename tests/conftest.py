import asyncio
from datetime import datetime

import pytest
from asyncpg import connect
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from api.main import app
from api.src.db.config import (
    create_async_sessionmaker,
    create_test_async_engine,
    get_db_sessionmaker,
)
from api.src.db.models import Base
from api.src.settings import settings
from api.src.weather.dependencies import get_weather_service
from api.src.weather.dummy import DummyWeatherService

async_engine = create_test_async_engine()
async_sessionmaker = create_async_sessionmaker(async_engine)


@pytest.fixture(scope="session")
async def init_db():
    """Создание тестового движка базы данных."""
    ap_conn = await connect(
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME[5:],
    )
    db_exists = await ap_conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname=$1", settings.DB_NAME
    )
    if not db_exists:
        await ap_conn.execute(f"CREATE DATABASE {settings.DB_NAME}")
    await ap_conn.close()

    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
    yield async_sessionmaker
    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_client():
    app.dependency_overrides[get_db_sessionmaker] = lambda: async_sessionmaker
    app.dependency_overrides[get_weather_service] = lambda: DummyWeatherService
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def clear_data():
    async with async_engine.begin() as session:
        for table in Base.metadata.sorted_tables:
            await session.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;")
            )


@pytest.fixture(scope="function")
async def query1():
    return {
        "city": "Minsk",
        "temp": 271.77,
        "wind_speed": 3.42,
        "wind_degree": 149,
        "humidity": 68,
        "description": "overcast clouds",
        "pressure": 1023,
        "created_at": datetime.strptime("2025-02-26T22:57:45", "%Y-%m-%dT%H:%M:%S"),
    }


@pytest.fixture(scope="function")
async def query2():
    return {
        "city": "Oslo",
        "temp": 271.77,
        "wind_speed": 3.42,
        "wind_degree": 149,
        "humidity": 68,
        "description": "overcast clouds",
        "pressure": 1023,
        "created_at": datetime.strptime("2025-02-26T22:57:45", "%Y-%m-%dT%H:%M:%S"),
    }


@pytest.fixture(scope="function")
async def query3():
    return lambda city: {
        "city": city,
        "description": "Lorem ipsum",
        "wind_speed": 42.0,
        "wind_degree": 24,
        "temp": 228.0,
        "humidity": 52,
        "pressure": 1337,
    }
