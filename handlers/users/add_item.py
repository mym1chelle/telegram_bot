# Добавление товара через бота. Чтобы не каждый пользователь имел ввозможность добавлять товар, в базе данных создана таблица администраторов, откуда реализует работу фильтр
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from utils.db_api import db_commands as commands
from states import AddItems
from filters import AdminFilter
from keyboards.inline.admin_menu import admin_keyboard
from keyboards.inline.start_keyboard import start_keyboard



@dp.message_handler(Command('admin'), AdminFilter())
async def admin_settings(message: types.Message):
    await message.answer(f'{message.from_user.get_mention()}, вы вошли в меню администратора:\n', reply_markup=admin_keyboard)

@dp.callback_query_handler(text='add_item')
async def add_item(call: types.CallbackQuery):
    await call.message.answer('Название товара')
    await AddItems.enter_name.set()

@dp.message_handler(state=AddItems.enter_name)
async def enter_name(message: types.Message, state: FSMContext):
    item_name = message.text
    
    async with state.proxy() as data:
        data['item_name'] = item_name

    await message.answer('Цена')
    await AddItems.enter_price.set()


@dp.message_handler(state=AddItems.enter_price)
async def enter_price(message: types.Message, state: FSMContext):
    item_price = message.text
    
    async with state.proxy() as data:
        data['item_price'] = item_price

    await message.answer('Описание')
    await AddItems.enter_description.set()


@dp.message_handler(state=AddItems.enter_description)
async def enter_description(message: types.Message, state: FSMContext):
    item_description = message.text
    
    async with state.proxy() as data:
        data['item_description'] = item_description

    await message.answer('Код категории')
    await AddItems.enter_category_code.set()


@dp.message_handler(state=AddItems.enter_category_code)
async def enter_category_code(message: types.Message, state: FSMContext):
    item_category_code = message.text
    
    async with state.proxy() as data:
        data['item_category_code'] = item_category_code

    await message.answer('Имя категории')
    await AddItems.enter_category_name.set()


@dp.message_handler(state=AddItems.enter_category_name)
async def enter_category_name(message: types.Message, state: FSMContext):
    item_category_name = message.text
    
    async with state.proxy() as data:
        data['item_category_name'] = item_category_name

    await message.answer('Код подкатегории')
    await AddItems.enter_subcategory_code.set()


@dp.message_handler(state=AddItems.enter_subcategory_code)
async def enter_subcategory_code(message: types.Message, state: FSMContext):
    item_subcategory_code = message.text
    
    async with state.proxy() as data:
        data['item_subcategory_code'] = item_subcategory_code

    await message.answer('Имя подкатегории')
    await AddItems.enter_subcategory_name.set()


@dp.message_handler(state=AddItems.enter_subcategory_name)
async def enter_subcategory_name(message: types.Message, state: FSMContext):
    item_subcategory_name = message.text
    
    data = await state.get_data()

    item_name = data.get('item_name')
    item_price = data.get('item_price')
    item_description = data.get('item_description')
    item_category_code = data.get('item_category_code')
    item_category_name = data.get('item_category_name')
    item_subcategory_code = data.get('item_subcategory_code')
    
  
    result = await commands.add_item(name=item_name, price=item_price, description=item_description, category_code=item_category_code, category_name=item_category_name, subcategory_code=item_subcategory_code, subcategory_name=item_subcategory_name)
    if result==False:
        await bot.send_message(chat_id=message.from_user.id, text=f'Произошла ошибка при добавлении товара. Товар не был добавлен.')
        
    else:
        await bot.send_message(chat_id=message.from_user.id, 
        text=f'Товар: {item_name}\n'
        f'Описание: {item_description}\n'
        f'Цена: {item_price}\n'
        f'успешно добавлен.',
        reply_markup=start_keyboard)
    await state.finish()