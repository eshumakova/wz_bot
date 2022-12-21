import aiohttp
from datetime import datetime
from .variables import WEATHER_TOKEN


def parse_weather_data(data: dict, name: bool) -> str:
    weather = ", ".join(f"{i['description']}" for i in data["weather"])
    weather_info = f"🔭 Погода в городе {data['name']}: {weather}." if name else ""
    weather_info += f"""
🖼 Температура: {data['main']['temp']}°C.
🔴 Ощущается как: {data['main']['feels_like']}°C.
🔆 Влажность: {data['main']['humidity']}%.
📝 Давление: {data['main']['pressure']} мм.рт.ст.
    """
    return weather_info


def parse_day_weather_data(data: dict) -> str:
    weather_info = ""
    for i in data['list'][:8]:
        weather_info += datetime.fromtimestamp(i['dt']).strftime('%H:%M:%S') + ' ' + '{0:+3.0f}'.format(
            i['main']['temp']) + ' ' + i['weather'][0]['description'] + "\n"

    return weather_info


async def get_weather(url, worker, *args) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data["cod"] == "404":
                return "Город не найден"
            return worker(data, *args)


async def get_current_weather(city: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}&units=metric&lang=ru"
    return await get_weather(url, parse_weather_data, True)


async def get_day_weather(city: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_TOKEN}&units=metric&lang=ru"
    return await get_weather(url, parse_day_weather_data)


async def get_weather_by_coords(lat: str, lon: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}&units=metric&lang=ru"
    return await get_weather(url, parse_weather_data, False)
