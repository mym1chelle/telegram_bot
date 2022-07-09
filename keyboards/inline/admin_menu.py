from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить товар', callback_data='add_item'),
                
           InlineKeyboardButton(text='Редактировать товар', switch_inline_query_current_chat='')
        ]
    ]
)