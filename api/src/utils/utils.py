import httpx

from api.src.exceptions import CityDoesntExist
from api.src.settings import settings


def remove_none_values(data):
    return {key: value for key, value in data.items() if value is not None}


async def request_weather(city: str):
    async with httpx.AsyncClient() as cl:
        req = await cl.get(
            f"{settings.API_URL}find?q={city}&APPID={settings.API_TOKEN}"
        )
        if req.status_code == 404:
            raise CityDoesntExist

        info = req.json()[0]
        return {
            "city": info["name"],
            "description": info["weather"][0]["description"],
            "wind_speed": info["wind"]["speed"],
            "wind_degree": info["wind"]["deg"],
            "wind_gust": info["wind"]["gust"],
            "temp": info["temp"],
            "humidity": info["humidity"],
            "pressure": info["pressure"],
        }
