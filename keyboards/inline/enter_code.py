from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

enter_code = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Ввести код',
                callback_data='code'),

            
             InlineKeyboardButton(
                text='Проверить подписки',
                callback_data='check_subs'),
        ]
    ]
)