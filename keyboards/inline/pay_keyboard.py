# кнопка для начала оплаты товара
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

pay_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Оплатить товар',
                callback_data='pay'),
        ]
    ]
)