from datetime import date

from fastapi import APIRouter
from fastapi import Depends

from src.config.database import get_session
from src.schemas.weather import WeatherStatsSchema
from src.services.weather import WeatherService

stats_router = APIRouter(tags=['Stats'])


@stats_router.get("/", name="Средняя температура и влажность за период по городу", response_model=WeatherStatsSchema)
async def get_weather_stats_in_range(city: str, start_date: date, end_date: date = None, session=Depends(get_session)):
    return await WeatherService(session).get_average_stats_in_range(city, start_date, end_date)
