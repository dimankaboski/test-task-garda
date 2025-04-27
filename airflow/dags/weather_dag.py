from datetime import datetime
import json
import os
import pendulum
import asyncio

from airflow.sdk import dag, task, Variable
from weather_api.services.weather import WeatherService, OpenWeatherMapAPI

from weather_api.schemas.weather import WeatherDataCreateSchema


# from weather_api.database.models import WeatherData


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
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
    def transform(weather_data: dict) -> list:
        response = []
        for el in weather_data:
            response.append(WeatherDataCreateSchema(city=el['name'],
                                                    temperature=el['main']['temp'],
                                                    humidity=el['main']['humidity'],
                                                    date=datetime.now().date()))
        print(response)
        return response

    @task()
    def load(schemas: list) -> None:
        print(f"Last task")

    weather_data = extract()
    data = transform(weather_data)
    load(data)


weather_update_data_task()
