# прописываем реакцию на кнопку «Купить»
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async
from data.config import PROVIDER_TOKEN
from utils.misc.shipping import *
from utils.misc.converter import converter


from keyboards.inline.menu_keyboard import buy_item
from keyboards.inline.pay_keyboard import pay_keyboard
from keyboards.inline.start_keyboard import start_keyboard
from loader import dp, bot
from utils.db_api.db_commands import get_purchase, select_user, get_item
from django_project.telegrambot.usermanage.models import Purchase


@dp.callback_query_handler(buy_item.filter())
async def enter_buy(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data.get('item_id') # беру id товара у которого была нажата кнопка купить
    user = await select_user(call.from_user.id)
    item = await get_item(item_id) # сохраняю все информацию о товаре по его id

    # создаю саму покупку
    purchase = Purchase()
    purchase.buyer_id = user.id
    purchase.item_id_id = int(item_id)
    purchase.reciever = call.from_user.full_name

    await state.update_data(purchase=purchase, item=item) # сохраняю данные о товаре и заказе с помощью машины состояний
    await bot.send_message(text='Введите количество товара', chat_id=call.from_user.id)
    await state.set_state('enter_quantity') # осуществляю переход к другому состоянию


@dp.message_handler(state='enter_quantity')
async def enter_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer('Неверное значение, введите заново')
        return

    async with state.proxy() as data:
        # сохраняю в состояние информацию о введенном количестве товара и его цене
        data['purchase'].quantity = quantity
        data['purchase'].amount = quantity * data['item'].price

    await message.answer('Отправьте свой номер телефона', reply_markup=ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton('Отправить номер', request_contact=True)  # забираем номер из аккаунта пользователя
        ]], resize_keyboard=True
    ))
    await state.set_state('enter_phone')

@dp.message_handler(state='enter_phone', content_types=types.ContentTypes.CONTACT)
async def enter_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    data = await state.get_data()
    purchase = data.get('purchase') # достаю информацию о заказе
    purchase.phone_number = phone_number # добавляю к ней номер телефона заказчика
    await sync_to_async(purchase.save)()
    await state.finish()
    await message.answer('Покупка создана.', reply_markup=pay_keyboard)


@dp.callback_query_handler(text='pay')
async def pay_item(call: types.CallbackQuery):
    user = await select_user(call.from_user.id) # собираю иформацию о польователе, который нажал кнопку купить
    purchase = await get_purchase(user_id = user.id) # беру из БД последний заказ данного пользователя

    if purchase.successful == False:
        # если заказ не оплачен
        item = await get_item(item_id=purchase.item_id_id) # собираю информацию о товаре в заказе
        # оформляю инвойс на оплату выбранного товара
        await bot.send_invoice(chat_id=call.from_user.id,
                                title=item.name,
                                description=item.description,
                                provider_token=PROVIDER_TOKEN,
                                currency='RUB',
                                prices=[
                                    types.LabeledPrice(label=item.name, amount=int(converter(purchase.amount))),
                                    types.LabeledPrice(label='Скидка', amount=-(int(converter(user.bonus)))),
                                ],
                                need_shipping_address=True,
                                start_parameter=f'create_invoice_{item.id}',
                                is_flexible=True,
                                payload='12345'

        )
    else:
        # если товар уже оплачен, то не допускаю повторной оплаты
        await call.message.answer(f'Этот товар уже оплачен.', reply_markup=start_keyboard)


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    """
    Позволяет выбрать условие доставки
    """

    if query.shipping_address.country_code == 'RU':
        await bot.answer_shipping_query(shipping_query_id=query.id, shipping_options=[
            POST_FAST_SHIPPING, POST_REGULAR_SHIPPING, PICKUP_SHIPPING], ok=True)
    elif query.shipping_address.country_code == 'US':
        await bot.answer_shipping_query(shipping_query_id=query.id, ok=False, error_message='В данной стране невозможно оформить доставку.')
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id, shipping_options=[
            POST_REGULAR_SHIPPING
        ], ok=True)

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(query: types.PreCheckoutQuery):
    # произведение оплаты
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
  

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    # проверка на удачное осуществление оплаты
    user = await select_user(message.from_user.id)

    if user.bonus != 0:
        # обнуляю бонусные баллы, если они есть у пользователя
        user.bonus = 0 
        await sync_to_async(user.save)()

    purchase = await get_purchase(user_id = user.id)
    # обновляю статус оплаты в заказе
    purchase.successful = True
    await sync_to_async(purchase.save)()

    if message.successful_payment.provider_payment_charge_id:
        await bot.send_message(chat_id=message.from_user.id,
            text=f'Спасибо, {message.from_user.get_mention()}! Вы оплатили товар на сумму {message.successful_payment.total_amount} {message.successful_payment.currency}. Ожидайте звонка оператора.'
        )
