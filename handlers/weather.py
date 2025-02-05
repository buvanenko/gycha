import asyncio

import aiohttp
import config

import sber

async def get_location(city: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={config.OW_TOKEN}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            data = await response.json()
            if len(data) == 0:
                return None
            return data[0]['lat'], data[0]['lon']


async def get_weather(lat: float, lon: float):
    url = f"http://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}&lon={lon}&appid={config.OW_TOKEN}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            data = await response.json()
            return data

async def get(city: str):
    lat, lon = await get_location(city)
    if lat is None:
        return None
    data = await get_weather(lat, lon)
    answer = await sber.chat.weather(data)
    return answer