from api.src.dao.queries import QueriesDAO
from api.src.schemas.queries import DisplayQuery


async def test_add_query(init_db, query1):
    async with init_db() as session:
        res = await QueriesDAO.add(session, **query1)

    res_dict = DisplayQuery.model_validate(res).model_dump()
    del res_dict["id"]
    assert res_dict == query1


async def test_find_queries(init_db, query1, query2):
    async with init_db() as session:
        queries_list = [query1, query2]
        res = []
        for el in queries_list:
            res.append(await QueriesDAO.add(session, **el))

        res_dicts = []
        for i, el in enumerate(res):
            res_dicts.append(DisplayQuery.model_validate(el).model_dump())
            del res_dicts[i]["id"]
            assert res_dicts[i] == queries_list[i]

        assert len(res_dicts) == 2

        find_all_res = await QueriesDAO.find_all(session)
        assert len(find_all_res) == 2

        find_query1_res = await QueriesDAO.find_all(session, city=query1["city"])
        assert len(find_query1_res) == 1
        assert find_query1_res[0].city == query1["city"]

        find_offset_res = await QueriesDAO.find_all(session, offset=1)
        assert len(find_offset_res) == 1

        find_limit_res = await QueriesDAO.find_all(session, limit=1)
        assert len(find_limit_res) == 1

        find_limit_offset_res = await QueriesDAO.find_all(session, limit=1, offset=1)
        assert len(find_limit_offset_res) == 1
        assert find_limit_res != find_limit_offset_res
