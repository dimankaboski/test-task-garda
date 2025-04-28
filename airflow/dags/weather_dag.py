import os
import asyncio
import logging

from datetime import datetime, timedelta
from airflow.sdk import dag, task, Variable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from weather_api.services.weather import WeatherService, OpenWeatherMapAPI
from weather_api.schemas.weather import WeatherDataCreateSchema

from weather_models import WeatherData

logger = logging.getLogger(__name__)


@dag(
    schedule="0 12 * * *",
    catchup=False,
    tags=["api"],
)
def weather_update_data_task():
    @task()
    def extract() -> list:
        cities_list = ["London", "Moscow", "Tokyo"]
        provider = OpenWeatherMapAPI(key=os.getenv("OPEN_WEATHER_API_KEY"))
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(WeatherService(cities_list, provider).get_weather_info())
        return result

    @task()
    def transform(weather_data: list[dict]) -> list[dict]:
        response = []
        for el in weather_data:
            validated = WeatherDataCreateSchema(city=el['name'],
                                                temperature=el['main']['temp'],
                                                humidity=el['main']['humidity'],
                                                date=datetime.now().date())
            response.append(validated.model_dump())
        return response

    @task()
    def load(schemas: list) -> None:
        engine = create_engine(os.getenv("WEATHER_DATABASE__SQL_ALCHEMY_CONN"))
        Session = sessionmaker(bind=engine)
        session = Session()
        for item in schemas:
            weather_data_item = WeatherData(**item)
            session.add(weather_data_item)
        session.commit()
        session.close()

    @task()
    def verify_new_load() -> None:
        engine = create_engine(os.getenv("WEATHER_DATABASE__SQL_ALCHEMY_CONN"))
        Session = sessionmaker(bind=engine)
        session = Session()
        yesterday = datetime.utcnow().date() - timedelta(days=1)
        count = session.query(WeatherData).filter(WeatherData.date >= yesterday).count()
        if count == 0:
            logger.warning(f"No new weather data for {yesterday}")
        session.close()

    weather_data = extract()
    validated_data = transform(weather_data)
    loaded_data = load(validated_data)
    verify = verify_new_load()

    loaded_data >> verify


weather_update_data_task()
