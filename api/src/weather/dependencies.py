from fastapi import Request


def get_weather_service(request: Request):
    return request.state.weather_service
