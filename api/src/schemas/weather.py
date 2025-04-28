from datetime import datetime, date

from pydantic import BaseModel, Field, field_serializer


class WeatherDataCreateSchema(BaseModel):
    city: str
    date: date
    temperature: float
    humidity: int


class WeatherStatsSchema(BaseModel):
    city: str
    date_start: date
    date_end: date | None
    average_temperature: float
    average_humidity: float

    @field_serializer("average_temperature", when_used="json")
    def serialize_average_temperature(self, v):
        return round(v, 2)

    @field_serializer("average_humidity", when_used="json")
    def serialize_average_humidity(self, v):
        return round(v, 2)


class WeatherDaySchema(BaseModel):
    date: date
    temperature: float
    humidity: int


class WeatherDaysRangeSchema(BaseModel):
    city: str
    days: list[WeatherDaySchema]
