from typing import Any

import httpx

from api.src.exceptions import CityDoesntExist
from api.src.settings import settings
from api.src.weather.base import BaseWeatherService


class OWMWeatherService(BaseWeatherService):
    API_URL = "https://api.openweathermap.org/data/3/"

    @classmethod
    async def get_city_weather(cls, city: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as cl:
            req = await cl.get(f"{cls.API_URL}find?q={city}&APPID={settings.API_TOKEN}")
            if req.status_code == 404:
                raise CityDoesntExist

            info = req.json()[0]
            return {
                "city": info["name"],
                "description": info["weather"][0]["description"],
                "wind_speed": info["wind"]["speed"],
                "wind_degree": info["wind"]["deg"],
                "temp": info["temp"],
                "humidity": info["humidity"],
                "pressure": info["pressure"],
            }
