# Начальное меню
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Товары',
                switch_inline_query_current_chat=''),
                
            InlineKeyboardButton(
                text='Реферралы',
                callback_data='ref')
        ],

        [
            InlineKeyboardButton(
                text='Мои заказы',
                callback_data='order_list'),

            InlineKeyboardButton(
                text='Корзина',
                callback_data='cart')
        ]
    ]
)