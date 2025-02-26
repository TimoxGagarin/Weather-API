from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.src.dao.queries import QueriesDAO
from api.src.db.config import get_db_session
from api.src.settings import settings

router = APIRouter(prefix="", tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def root(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    page: int = 1,
    size: int = 10,
):
    queries = await QueriesDAO.find_all(session, offset=(page - 1) * size, limit=size)
    context = {
        "request": request,
        "queries": queries,
    }
    return settings.templates.TemplateResponse("main.html", context)
