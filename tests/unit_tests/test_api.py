from api.src.schemas.queries import DisplayQuery


async def test_add_query(init_db, async_client, query1, query3):
    res = await async_client.post("/queries", json={"city": query1["city"]})
    assert res.status_code == 201

    data = res.json()
    res_dict = DisplayQuery.model_validate(data).model_dump()

    del res_dict["id"]
    del res_dict["created_at"]
    assert res_dict == query3(query1["city"])


async def test_find_queries(init_db, async_client, query1, query2, query3):
    queries_list = [query3(query1["city"]), query3(query2["city"])]
    res = []
    for el in queries_list:
        resp = await async_client.post("/queries", json={"city": el["city"]})
        assert resp.status_code == 201
        res.append(resp.json())

    res_dicts = []
    for i, el in enumerate(res):
        res_dicts.append(DisplayQuery.model_validate(el).model_dump())
        del res_dicts[i]["id"]
        del res_dicts[i]["created_at"]
        assert res_dicts[i] == queries_list[i]

    assert len(res_dicts) == 2

    find_all_res = await async_client.get("/queries")
    assert find_all_res.status_code == 200
    assert len(find_all_res.json()) == 2

    find_query1_res = await async_client.get(
        "/queries", params={"city": query1["city"]}
    )
    assert find_all_res.status_code == 200
    assert len(find_query1_res.json()) == 1
    assert find_query1_res.json()[0]["city"] == query1["city"]

    find_offset_res = await async_client.get("/queries", params={"offset": 1})
    assert find_all_res.status_code == 200
    assert len(find_offset_res.json()) == 1

    find_limit_res = await async_client.get("/queries", params={"limit": 1})
    assert find_all_res.status_code == 200
    assert len(find_limit_res.json()) == 1

    find_limit_offset_res = await async_client.get(
        "/queries", params={"offset": 1, "limit": 1}
    )
    assert find_all_res.status_code == 200
    assert len(find_limit_offset_res.json()) == 1
    assert find_limit_res.json() != find_limit_offset_res.json()
