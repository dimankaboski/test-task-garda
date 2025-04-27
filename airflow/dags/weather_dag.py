import json
import os
import pendulum
import asyncio

from airflow.sdk import dag, task, Variable
from weather_api.services.weather import WeatherService, OpenWeatherMapAPI


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def weather_update_data_task():
    @task()
    def extract():
        cities_list = ["London", "Moscow", "Tokyo"]
        provider = OpenWeatherMapAPI(key=os.getenv("OPEN_WEATHER_API_KEY"))
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(WeatherService(cities_list, provider).get_weather_info())
        return result

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):
        print(f"Total order value is: {total_order_value:.2f}")

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])


weather_update_data_task()
