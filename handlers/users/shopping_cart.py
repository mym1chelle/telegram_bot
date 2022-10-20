
from utils.db_api import db_commands as commands
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncio import sleep

from keyboards.inline.pay_keyboard import pay_cart_keyboard
from keyboards.inline.cart_keyboard import cart_keyboard, plus, minus, item_quantity, delete_purchase
from keyboards.inline.start_keyboard import start_keyboard

@dp.callback_query_handler(text='cart')
async def wiev_cart(call: types.CallbackQuery):
    """Показывает товары в корзине, иначе говоря все неоплаченные товары пользователя"""
    await call.answer()
    user = await commands.select_user(call.from_user.id)
    purchase = await commands.select_unpaid_purchase(user_id=user.id)
    
    for i in purchase:
        quantity = await commands.get_purchase(purchase_id=i.id)
        if quantity.quantity == 0:
            await commands.delete_purchase(purchase_id=i.id)

    if not purchase.exists():
        try:
            await call.message.edit_text(f'В корзине нет товаров. ', reply_markup=start_keyboard)
        except:
            pass

    else:
        for i in purchase:
            purchase_id = i.id
            
            item = await commands.get_item(item_id=i.item_id.id)
            await call.message.answer(f'{i.item_id}: {i.amount} руб., ', reply_markup=cart_keyboard(quantity=i.quantity, purchase_id=purchase_id, price=item.price))

        total_sum = await commands.total_sum_unpaid_purchase(user_id=user.id)
        await call.message.answer(text=f'К оплате: {total_sum["amount__sum"]}', reply_markup=pay_cart_keyboard)

@dp.callback_query_handler(plus.filter())
async def increase(call: types.CallbackQuery, callback_data: dict):
    """Увеличивает количество товара в заказе"""
    await call.answer()
    await commands.increase(purchase_id=callback_data['purchase_id'], purchase_price=callback_data['price'])


@dp.callback_query_handler(minus.filter())
async def decrease(call: types.CallbackQuery, callback_data: dict):
    """Уменьшает количество товара в заказе"""
    await call.answer()
    await commands.decrease(purchase_id=callback_data['purchase_id'], purchase_price=callback_data['price'])


@dp.callback_query_handler(item_quantity.filter())
async def change_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """Изменение количества товара в заказе ручным вводом"""
    await call.answer()
    await call.message.answer('Введите нужное количество товара: ')
    async with state.proxy() as data:
        data['purchase_id'] = callback_data['purchase_id']
        data['price'] = callback_data['price']
    await state.set_state('new_quantity')

@dp.message_handler(state='new_quantity')
async def get_quantity(message: types.Message, state: FSMContext):
    quantity = int(message.text)

    data = await state.get_data()
    purchase_id = data.get('purchase_id')
    price = data.get('price')

    await commands.change_quantity(purchase_id=purchase_id, purchase_quantity=quantity, purchase_price=price)

    await state.finish()

@dp.callback_query_handler(delete_purchase.filter())
async def delete_purchase(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await commands.delete_purchase(purchase_id=callback_data['purchase_id'])
