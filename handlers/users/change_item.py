from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.menu_keyboard import edit_item_keyboard
from keyboards.inline.start_keyboard import start_keyboard
from keyboards.inline.menu_keyboard import change_item, del_item
from utils.db_api import db_commands as commands
from loader import dp, bot

@dp.callback_query_handler(del_item.filter())
async def delete_item(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    item_id = callback_data.get('item_id')
    item = await commands.get_item(item_id)
    await bot.send_message(chat_id=call.from_user.id, text=f'Вы действительно хотите удалить товар {item}?\n', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                    InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text='Нет', callback_data='no')]]) # подключаю клавиатуру для покупки
            )

    async with state.proxy() as data:
        data['item'] = item
    await state.set_state('check_delete_item')

@dp.callback_query_handler(state='check_delete_item', text='yes')
async def edit_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    name = item.name
    print(item.id)
    await commands.delete_item(item_id=item.id)
    await state.finish()
    await bot.send_message(chat_id=call.from_user.id, text=f'Вы удалили товар {name}.')

@dp.callback_query_handler(state='check_delete_item', text='no')
async def edit_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Вы отменили удаление товара {item.name}.', reply_markup=start_keyboard)

@dp.callback_query_handler(change_item.filter())
async def change_item(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    item_id = callback_data.get('item_id')
    item = await commands.get_item(item_id)
    await bot.send_message(chat_id=call.from_user.id, text=f'Что нужно изменить в товаре {item.name}?\n', reply_markup=edit_item_keyboard)
    async with state.proxy() as data:
        data['item'] = item
    await state.set_state('edit_item')

# изменение имени товара
@dp.callback_query_handler(state='edit_item', text='name')
async def edit_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Введите новое имя для товара {item.name}')
    await state.set_state('enter_new_name')

@dp.message_handler(state='enter_new_name')
async def edit_new_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('item')
    print(item.id)
    print(message.text)
    await commands.edit_name(item_id=item.id, new_name=message.text)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=f'Вы изменили товар. Новое имя товара {message.text}')
    
# изменение описания товара
@dp.callback_query_handler(state='edit_item', text='description')
async def edit_description(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Введите новое описание для товара {item.name}: {item.description}')
    await state.set_state('enter_new_description')

@dp.message_handler(state='enter_new_description')
async def edit_new_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('item')
    print(item.id)
    print(message.text)
    await commands.edit_description(item_id=item.id, new_description=message.text)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=f'Вы изменили описание товара. Новое описание товара {message.text}')

# изменение цены
@dp.callback_query_handler(state='edit_item', text='price')
async def edit_price(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Введите новую цену для товара {item.name}: {item.price}')
    await state.set_state('enter_new_price')

@dp.message_handler(state='enter_new_price')
async def edit_new_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('item')
    print(item.id)
    print(message.text)
    await commands.edit_price(item_id=item.id, new_price=message.text)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=f'Вы изменили цену товара. Новое цена товара {message.text}')

# изменение кода категории
@dp.callback_query_handler(state='edit_item', text='category_code')
async def edit_category_code(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Введите новый код категории для товара {item.name}: {item.category_code}')
    await state.set_state('enter_new_category_code')

@dp.message_handler(state='enter_new_category_code')
async def edit_new_category_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('item')
    print(item.id)
    print(message.text)
    await commands.edit_category_code(item_id=item.id, new_category_code=message.text)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=f'Вы изменили код категории товара. Новое код категории товара товара {message.text}')

# измененение имени категории
@dp.callback_query_handler(state='edit_item', text='category_name')
async def edit_category_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Введите новый код категории для товара {item.name}: {item.category_name}')
    await state.set_state('enter_new_category_name')

@dp.message_handler(state='enter_new_category_name')
async def edit_new_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('item')
    print(item.id)
    print(message.text)
    await commands.edit_category_name(item_id=item.id, new_category_name=message.text)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=f'Вы изменили имя категории товара. Новое имя категории товара {message.text}')

# изменение кода подкатегории
@dp.callback_query_handler(state='edit_item', text='subcategory_code')
async def edit_subcateory_code(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Введите новый код подкатегории для товара {item.name}: {item.subcategory_code}')
    await state.set_state('enter_new_subcategory_code')

@dp.message_handler(state='enter_new_subcategory_code')
async def edit_new_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('item')
    print(item.id)
    print(message.text)
    await commands.edit_subcategory_code(item_id=item.id, new_subcategory_code=message.text)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=f'Вы изменили код подкатегории товара. Новое код подкатегории товара {message.text}')

# изменение имени подкатегории
@dp.callback_query_handler(state='edit_item', text='subcategory_name')
async def edit_subcategory_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    item = data.get('item')
    await bot.send_message(chat_id=call.from_user.id, text=f'Введите новое имя подкатегории товара {item.name}: {item.subcategory_name}')
    await state.set_state('enter_new_subcategory_name')


@dp.message_handler(state='enter_new_subcategory_name')
async def edit_new_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get('item')
    print(item.id)
    print(message.text)
    await commands.edit_subcategory_name(item_id=item.id, new_subcategory_name=message.text)
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id, text=f'Вы изменили код подкатегории товара. Новое код подкатегории товара {message.text}')