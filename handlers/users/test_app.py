# Здесь я буду тестировать создание веб-приложения в telegram

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from data.config import APP_LINK

@dp.message_handler(commands='app')
async def start_app(message: types.Message):
    app = types.web_app_info.WebAppInfo
    await message.answer(
        'text',
        reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='test', web_app=app(url=APP_LINK)))
    )