from aiogram import types
from utils.db_api.db_commands import search_item
from loader import dp
# from keyboards.inline.menu_keyboard import buy_item_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Эта версия сразу для покупки товара бещ его перехода в чат с ботом
# @dp.inline_handler()
# async def item_query(query: types.InlineQuery):
#     items = await search_item(query.query)  # осуществляю поиск по товарам по вводу в инлайн режиме
#     results = []
#     # генерирую результат для каждого товара из списка
#     for item in items:
#         line = types.InlineQueryResultArticle(
#             id=item.id,
#             title=item.name,
#             description=item.description,
#             input_message_content=types.InputMessageContent(
#                 message_text=f'Название товара: {item.name}\n'
#                              f'Цена: {item.price}'),
#             reply_markup=buy_item_keyboard(item_id=item.id)  # подключаю клавиатуру для покупки
#             )
#         results.append(line)  # формирую список с окончательным результатом

#     await query.answer(results=results)



@dp.inline_handler()
async def item_query(query: types.InlineQuery):
    items = await search_item(query.query)  # осуществляю поиск по товарам по вводу в инлайн режиме
    results = []
    # генерирую результат для каждого товара из списка
    for item in items:
        line = types.InlineQueryResultArticle(
            id=item.id,
            title=item.name,
            description=item.description,
            input_message_content=types.InputMessageContent(
                message_text=f'Название товара: {item.name}'),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                    InlineKeyboardButton(text='Показать товар', url=f'https://t.me/Project_MyM1chelle_Bot?start={item.id}'),
                                    InlineKeyboardButton(text='Меню', switch_inline_query_current_chat='')]]) # подключаю клавиатуру для покупки
            )
        results.append(line)  # формирую список с окончательным результатом
    await query.answer(results=results)

