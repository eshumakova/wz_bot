import aioredis

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from typing import Any, Coroutine, Union

from .variables import (
    TG_TOKEN,
    REDIS_HOST,
    WELCOME_MESSAGE
)
from .keyboards import start_keyboard, get_weeather_keyboard
from .weather_worker import get_current_weather, get_day_weather, get_weather_by_coords

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()

redis = aioredis.from_url(REDIS_HOST)


class Form(StatesGroup):
    city = State()


async def start_input(message_object: Union[Message, CallbackQuery]) -> None:
    await Form.city.set()
    await message_object.reply("Введите название города")


async def send_weather(message_object: Union[Message, CallbackQuery], weather_worker: Coroutine[Any, Any, str]) -> None:
    user_city_bytes = await redis.execute_command("get", message_object.from_user.id)
    if user_city_bytes is not None:
        user_city = user_city_bytes.decode()
        weather = await weather_worker(user_city)
        await bot.send_message(
            message_object.from_user.id,
            weather,
        )
        return

    await start_input(message_object)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Отмена ввода города')


@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=start_keyboard
    )


@dp.callback_query_handler(text="get_weather")
@dp.message_handler(Text(equals="🔅 Узнать погоду", ignore_case=True))
async def get_weather(callback_query: CallbackQuery):
    await send_weather(callback_query, get_current_weather)


@dp.message_handler(Text(equals="📕 Погода на день", ignore_case=True))
async def get_weather(callback_query: CallbackQuery):
    await send_weather(callback_query, get_day_weather)


@dp.message_handler(commands=["change_city"])
@dp.message_handler(Text(equals="🔃 Другой город", ignore_case=True))
async def change_city(message: Message):
    await start_input(message)


@dp.message_handler(state=Form.city)
async def process_city(message: Message, state: FSMContext):
    await redis.execute_command("set", message.from_user.id, message.text)

    await message.reply(
        f"Твой город: {message.text}",
        reply_markup=get_weeather_keyboard
    )

    await state.finish()


@dp.message_handler(content_types=['location'])
async def get_location(message: Message):
    weather = await get_weather_by_coords(message.location.latitude, message.location.longitude)
    await message.reply(
        weather,
        reply_markup=get_weeather_keyboard
    )
