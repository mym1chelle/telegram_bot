from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

plus = CallbackData('plus', 'purchase_id', 'price')
minus = CallbackData('minus', 'purchase_id', 'price', 'quantity')
item_quantity = CallbackData('quantity', 'purchase_id', 'price')
delete_purchase = CallbackData('delete_purchase', 'purchase_id')

def cart_keyboard(purchase_id, quantity, price):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='➕', callback_data=plus.new(purchase_id=purchase_id, price=price)),
        InlineKeyboardButton(text=quantity, callback_data=item_quantity.new(purchase_id=purchase_id, price=price)),
        InlineKeyboardButton(text='➖', callback_data=minus.new(purchase_id=purchase_id, price=price, quantity=quantity)),
        InlineKeyboardButton(text='❌', callback_data=delete_purchase.new(purchase_id=purchase_id)),
    )
    return markup