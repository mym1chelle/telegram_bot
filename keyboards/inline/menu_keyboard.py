# кнопка покупки товара
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import BOT_LINK as link

buy_item = CallbackData('buy', 'item_id')


def buy_item_keyboard(item_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Купить', callback_data=buy_item.new(item_id=item_id)),
        InlineKeyboardButton(text='Меню', switch_inline_query_current_chat='')
    )
    return markup



change_item = CallbackData('change', 'item_id')
del_item = CallbackData('delete', 'item_id')

def change_item_keyboard(item_id):
    markup = InlineKeyboardMarkup(row_width=4)
    markup.row(
        InlineKeyboardButton(text='Показать товар', url=f'{link}?start={item_id}'),
        InlineKeyboardButton(text='Меню', switch_inline_query_current_chat=''))
    markup.row(
        InlineKeyboardButton(text='Редактировать', callback_data=change_item.new(item_id=item_id)),
        InlineKeyboardButton(text='Удалить',  callback_data=del_item.new(item_id=item_id))
    )
    return markup



edit_item_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Имя', callback_data='name'),
            InlineKeyboardButton(text='Описание', callback_data='description'), 
            InlineKeyboardButton(text='Цена', callback_data='price')
        ],
        [
            InlineKeyboardButton(text='Код категории', callback_data='category_code'),
            InlineKeyboardButton(text='Название категории',  callback_data='category_name'),
        ],
        [
            InlineKeyboardButton(text='Код подкатегории', callback_data='subcategory_code'),
            InlineKeyboardButton(text='Название подкатегории',  callback_data='subcategory_name')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_edit')
        ]
    ]
)