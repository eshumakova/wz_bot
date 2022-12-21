from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Узнать погоду",
                                 callback_data="get_weather"),
        ]
    ]
)

get_weeather_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔃 Другой город"),
            KeyboardButton(text="🔅 Узнать погоду")
        ],
        [
            KeyboardButton(text="📌 По геопозиции", request_location=True),
            KeyboardButton(text="📕 Погода на день")
        ]
    ],
    resize_keyboard=True
)
