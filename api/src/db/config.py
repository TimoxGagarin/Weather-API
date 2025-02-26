from typing import AsyncGenerator, TypeAlias

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from api.src.settings import settings

AsyncSessionMaker: TypeAlias = async_sessionmaker[AsyncSession]


def create_async_engine() -> AsyncEngine:
    return _create_async_engine(
        url=settings.database_url,
        echo=settings.DEBUG,
        pool_size=settings.DATABASE_POOL_SIZE,
        pool_recycle=settings.DATABASE_POOL_RECYCLE_SECONDS,
    )


def create_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_sessionmaker(
    request: Request,
) -> AsyncGenerator[AsyncSessionMaker, None]:
    async_sessionmaker: AsyncSessionMaker = request.state.async_sessionmaker
    yield async_sessionmaker


async def get_db_session(
    request: Request,
    sessionmaker: AsyncSessionMaker = Depends(get_db_sessionmaker),
) -> AsyncGenerator[AsyncSession, None]:
    if session := getattr(request.state, "session", None):
        yield session
    else:
        async with sessionmaker() as session:
            try:
                request.state.session = session
                yield session
            except:
                await session.rollback()
                raise
            else:
                await session.commit()
