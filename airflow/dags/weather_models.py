from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    func,
    Float,
    Date
)

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    city = Column(String(300), nullable=False)
    date = Column(Date(), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
