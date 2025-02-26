from typing import Any

from api.src.weather.base import BaseWeatherService


class DummyWeatherService(BaseWeatherService):
    API_URL = None

    @classmethod
    async def get_city_weather(cls, city: str) -> dict[str, Any]:
        return {
            "city": city,
            "description": "Lorem ipsum",
            "wind_speed": 42,
            "wind_degree": 24,
            "temp": 228,
            "humidity": 52,
            "pressure": 1337,
        }
