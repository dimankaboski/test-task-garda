import logging

from datetime import date, datetime

from fastapi.exceptions import RequestValidationError, HTTPException

from src.schemas.weather import WeatherDaysRangeSchema, WeatherDaySchema, WeatherStatsSchema
from src.database.repositories import WeatherRepository
from src.utils.cache import RedisCache

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, session):
        self.repository = WeatherRepository(session)
        self.cache = RedisCache()

    async def validate_date(self, start_date: date, end_date: date) -> None:
        if start_date >= datetime.now().date():
            raise RequestValidationError("Enter a valid date")
        if end_date and end_date <= start_date:
            raise RequestValidationError("end_date must be grater than start_date")

    async def get_weather_in_range(self, city: str, date_start: date, date_end: date = None) -> WeatherDaysRangeSchema:
        await self.validate_date(date_start, date_end)
        cached = self.cache.get_cached(city, date_start, date_end, "weather")
        if cached:
            return WeatherDaysRangeSchema.model_validate(cached)
        data = await self.repository.get_weather_in_range(city, date_start, date_end)
        if not data:
            raise HTTPException(404, "Info not found")
        weather_days = [
            WeatherDaySchema(
                date=el.date,
                temperature=el.temperature,
                humidity=el.humidity
            )
            for el in data
        ]
        schema_data = WeatherDaysRangeSchema(city=city, days=weather_days)
        self.cache.set_cache(city, date_start, date_end, "weather", schema_data.model_dump(mode="json"))
        return schema_data

    async def get_average_stats_in_range(self, city: str, date_start: date,
                                         date_end: date = None) -> WeatherStatsSchema:
        cached = self.cache.get_cached(city, date_start, date_end, "average_stats")
        if cached:
            return WeatherStatsSchema.model_validate(cached)
        await self.validate_date(date_start, date_end)
        data = await self.repository.get_average_stats_in_range(city, date_start, date_end)
        if not any(data):
            raise HTTPException(404, "Info not found")
        schema_data = WeatherStatsSchema(city=city, date_start=date_start, date_end=date_end,
                                         average_temperature=data[0], average_humidity=data[1])
        self.cache.set_cache(city, date_start, date_end, "average_stats", schema_data.model_dump(mode="json"))
        return schema_data
