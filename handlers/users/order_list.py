from aiogram import types
from utils.db_api import db_commands as commands
from loader import dp
from keyboards.inline.start_keyboard import start_keyboard


# Эту функцию вы перспективе нужно удалить
@dp.callback_query_handler(text='order_list')
async def select_purchase(call: types.CallbackQuery):
    """Выводит список всех заказов пользователя. Одинаковые товары группирует по названию и выводит общую сумму и количество"""
    await call.answer()
    user = await commands.select_user(call.from_user.id)
    purchase = await commands.count_sum(user_id=user.id)
    # Это костыль. Нужно разобраться как узнавать товар по id более грамонтно.
    for i in purchase:
        item = await commands.get_item(item_id=i['item_id'])
        i['item_id'] = item.name
    purchase_lst = [f'{i["item_id"]}, цена: {i["total"]} руб., {i["quantity"]} шт.' for i in purchase]
    purchase_str = '\n'.join(purchase_lst)
    try:
        await call.message.edit_text(f'Вы заказали: \n{purchase_str}', reply_markup=start_keyboard)
    except:
        pass