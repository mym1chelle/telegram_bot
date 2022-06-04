# прописываем реакцию на кнопку «Купить»
from this import s
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async

from keyboards.inline.menu_keyboard import buy_item
from keyboards.inline.start_keyboard import start_keyboard
from loader import dp, bot
from utils.db_api.db_commands import select_user, get_item, add_item
from django_project.telegrambot.usermanage.models import Purchase


@dp.callback_query_handler(buy_item.filter())
async def enter_buy(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data.get('item_id')
    user = await select_user(call.from_user.id)
    print(user)
    item = await get_item(item_id)

    # создаю саму покупку
    purchase = Purchase()
    purchase.buyer_id = user.id
    purchase.item_id_id = int(item_id)
    purchase.reciever = call.from_user.full_name

    await state.update_data(purchase=purchase, item=item)

    # await call.message.answer('Введите количество товара')
    await bot.send_message(text='Введите количество товара', chat_id=call.from_user.id)
    await state.set_state('enter_quantity')


@dp.message_handler(state='enter_quantity')
async def enter_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer('Неверное значение, введите заново')
        return

    async with state.proxy() as data:
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
    purchase = data.get('purchase')
    purchase.phone_number = phone_number
    await sync_to_async(purchase.save)()
    await state.finish()
    await message.answer('Покупка создана.', reply_markup=start_keyboard)
