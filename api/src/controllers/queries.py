from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.src.dao.queries import QueriesDAO
from api.src.db.config import get_db_session
from api.src.schemas.queries import CreateQuery, DisplayQuery, SearchQuery
from api.src.utils.utils import remove_none_values
from api.src.weather.base import BaseWeatherService
from api.src.weather.dependencies import get_weather_service

router = APIRouter(prefix="/queries", tags=["queries"])


@router.get("")
async def find_all_queries(
    data: SearchQuery = Query(), session: AsyncSession = Depends(get_db_session)
) -> list[DisplayQuery]:
    return await QueriesDAO.find_all(session, **remove_none_values(data.model_dump()))


@router.post("", status_code=status.HTTP_201_CREATED)
async def search_weather(
    data: CreateQuery,
    session: AsyncSession = Depends(get_db_session),
    weather_service: BaseWeatherService = Depends(get_weather_service),
) -> DisplayQuery:
    data = await weather_service.get_city_weather(data.city)
    return await QueriesDAO.add(session, **data)
