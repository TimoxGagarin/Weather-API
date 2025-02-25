from fastapi import APIRouter, Query, status

from api.src.dao.queries import QueriesDAO
from api.src.schemas.queries import CreateQuery, DisplayQuery, SearchQuery
from api.src.utils.utils import remove_none_values, request_weather

router = APIRouter(prefix="/queries", tags=["queries"])


@router.get("")
async def find_all_queries(
    data: SearchQuery = Query(),
) -> list[DisplayQuery]:
    return await QueriesDAO.find_all(**remove_none_values(data.model_dump()))


@router.post("", status_code=status.HTTP_201_CREATED)
async def search_weather(data: CreateQuery) -> DisplayQuery:
    data = await request_weather(data.city)
    return await QueriesDAO.add(**data)
