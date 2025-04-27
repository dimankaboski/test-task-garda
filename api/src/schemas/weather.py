from datetime import datetime, date

from pydantic import BaseModel, Field


class WeatherDataCreateSchema(BaseModel):
    city: str
    date: date
    temperature: float
    humidity: int
