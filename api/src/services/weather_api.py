from aiohttp import ClientSession
from abc import ABC, abstractmethod


class WeatherAPI(ABC):
    @abstractmethod
    async def get_data_by_city(self, city: str) -> dict:
        raise NotImplementedError


class OpenWeatherMapAPI(WeatherAPI):
    def __init__(self, key: str, units: str = 'metric'):
        self.url = "https://api.openweathermap.org/data/2.5/weather/"
        self.key = key
        self.units = units

    async def get_data_by_city(self, city: str):
        async with ClientSession(base_url=self.url) as session:
            response = await session.request("GET", f'?appid={self.key}&units={self.units}&q={city}', ssl=False)
        return await response.json()


class WeatherAPIService:
    def __init__(self, cities: list[str], provider: WeatherAPI):
        self.cities = cities
        self.provider = provider

    async def get_weather_info(self):
        data = []
        for city in self.cities:
            data.append(await self.provider.get_data_by_city(city))
        return data
