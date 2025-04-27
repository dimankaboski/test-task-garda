import os
from api.src.services.weather import WeatherService, OpenWeatherMapAPI


def get_weather_data():
    cities_list = ["London", "Moscow", "Tokyo"]
    provider = OpenWeatherMapAPI(key=os.getenv("OPENWEATHER_API_KEY"))
    data = WeatherService(cities_list, provider).get_weather_info()
    print(data)
