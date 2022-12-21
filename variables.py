import dotenv
import os

dotenv.load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST")

WELCOME_MESSAGE = "👋 Привет! Я бот, который поможет тебе узнать погоду в любом городе. Напиши мне название города, и я покажу тебе погоду в нём."
