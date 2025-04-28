from datetime import date

from fastapi import APIRouter
from fastapi import Depends

from src.config.database import get_session
from src.schemas.weather import WeatherDaysRangeSchema
from src.services.weather import WeatherService

weather_router = APIRouter(tags=['Weather'])


@weather_router.get("/", name="Погода в указанный период по городу", response_model=WeatherDaysRangeSchema)
async def get_weather_in_range(city: str, start_date: date, end_date: date = None, session=Depends(get_session)):
    return await WeatherService(session).get_weather_in_range(city, start_date, end_date)
