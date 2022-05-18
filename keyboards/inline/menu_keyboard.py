# кнопка покупки товара
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


buy_item = CallbackData('buy', 'item_id')


def buy_item_keyboard(item_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Купить', callback_data=buy_item.new(item_id=item_id))
    )
    return markup