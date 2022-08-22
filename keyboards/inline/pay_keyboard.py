# кнопка для начала оплаты товаров в корзине
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

pay_cart_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Оплатить',
                callback_data='pay_cart'),
        ],
    ]
)