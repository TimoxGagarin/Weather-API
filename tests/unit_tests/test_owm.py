import pytest
from faker import Faker
from fastapi import HTTPException

from api.src.exceptions import CityDoesntExist
from api.src.schemas.queries import DisplayQuery
from api.src.weather.owm import OWMWeatherService


async def test_get_weather(query1):
    res = await OWMWeatherService.get_city_weather(query1["city"])
    assert res["city"] == query1["city"]

    faker = Faker()
    res["id"] = faker.uuid4()
    res["created_at"] = faker.date_time()

    assert DisplayQuery.model_validate(res)

    with pytest.raises(HTTPException) as exc_info:
        res = await OWMWeatherService.get_city_weather("string")
        assert exc_info == CityDoesntExist.detail
