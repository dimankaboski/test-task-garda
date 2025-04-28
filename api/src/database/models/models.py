from datetime import date, datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, Float, Date, Index
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column

from src.database.models.base import Base


class WeatherData(Base):
    __tablename__ = 'weather_data'
    __table_args__ = (
        Index('idx_city_date', 'city', 'date'),  # Составной индекс
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date(), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
