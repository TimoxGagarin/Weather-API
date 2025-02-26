from typing import Any, Protocol


class BaseWeatherService(Protocol):
    API_URL = None

    @classmethod
    async def get_city_weather(cls, city: str) -> dict[str, Any]:
        raise
