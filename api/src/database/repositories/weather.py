import logging

from abc import ABC
from datetime import date

from sqlalchemy import select, func
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.models import WeatherData

logger = logging.getLogger(__name__)


class AbstractRepository(ABC): ...


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self._session = session


class WeatherRepository(SQLAlchemyRepository):
    async def get_weather_in_range(self, city: str, date_start: date, date_end: date = None):
        query = (select(WeatherData).where(WeatherData.city == city).where(WeatherData.date >= date_start)
                 .order_by(WeatherData.date)
                 .options(load_only(WeatherData.date, WeatherData.temperature, WeatherData.humidity)))
        if date_end:
            query = query.where(WeatherData.date <= date_end)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_average_stats_in_range(self, city: str, date_start: date, date_end: date = None):
        query = (select(
            func.avg(WeatherData.temperature).label("average_temperature"),
            func.avg(WeatherData.humidity).label("average_humidity"))
                 .where(WeatherData.city == city)
                 .where(WeatherData.date >= date_start))
        if date_end:
            query = query.where(WeatherData.date <= date_end)
        result = await self._session.execute(query)
        data = result.first()
        return data
