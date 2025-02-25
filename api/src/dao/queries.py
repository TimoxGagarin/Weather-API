from api.src.dao.base import BaseDAO
from api.src.db.models import Queries


class QueriesDAO(BaseDAO):
    model = Queries
