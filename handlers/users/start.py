# 12.06.21 Работает подключение к базе данных и по реферальной ссылке и с помощью кода ввода.


from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api import db_commands as commands
from loader import dp, bot
from filters import UserFilter
import re

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link

from data.config import SECRET_CODE
from keyboards.inline.enter_code import enter_code
from utils.misc.referal_link_generator import gen_ref_link


# Версия 1 (рабочая):
# Работает добавление пользователя в БД и создание рефералов.
# Меню покупки товаров также работает
# 12.06.21 интегрировал её части для работы в следующей версии
# @dp.message_handler(CommandStart())
# async def register_user(message: types.Message):
#     referral = message.get_args()
#     await commands.add_user(user_id=message.from_user.id,
#                             full_name=message.from_user.full_name,
#                             username=message.from_user.username)
#     bot_username = (await bot.get_me()).username
#
#     # AttributeError: 'NoneType' object has no attribute 'id'
#
#     id_referral = (await commands.get_id(user_id=message.from_user.id)).id
#     bot_link = f'https://t.me/{bot_username}?start={id_referral}'
#     count = await commands.count_users()
#     await message.answer(
#         '\n'.join(
#             [
#                 f'Привет, {message.from_user.get_mention()}! '
#                 f'Ты был занесён в базу. '
#                 f'В базе <b>{count}</b> пользователей. '
#                 f'Твоя реферальная ссылка: {bot_link}'
#             ]
#         )
#     )
#
#     if referral:
#         await commands.add_referral(id=id_referral, referrer_id=referral)
# Почему то нельзя автоматически менять id_referral у ссылки и всегда там стоит 1


# Версия 2: Неверно работает регулярное выражение (добавление происходит и в случае когда я ввел 5 цифр)
# @dp.message_handler(CommandStart(deep_link=re.compile(r'\d\d\d\d')))
# async def register_user_deeplink(message: types.Message):
#     """Функция добавляет нового пользователя в базу данных для работы с ботом, если он ввел код доступа"""
#     await commands.add_user(user_id=message.from_user.id,
#                             full_name=message.from_user.full_name,
#                             username=message.from_user.username)
#     await message.answer(f'Привет, {message.from_user.get_mention()}!'
#                          f'Ты зашёл по реферальной ссылке {message.get_args()} и был добавлен в базу данных.')


# Схема работы:
# — нажимаю команду /start
# — проверяю есть ли пользователь в БД (для начала в самом хендлере, затем в middleware)
# — если нет, вывожу ему сообщение о том, что для регистрации нужна ссылка или код доступа, выбрасываю кнопку ввести код
# ✓ вводит код — регестрирую и выдаю его реферальную ссылку
# ✓ переходит по ссылке — регистрирую и выдаю его реферальную ссылку

# Версия 3: интегрирована с Версией 1 и работаю все три ситуации  (проверял только с 1 аккаунта)
@dp.message_handler(CommandStart(), UserFilter())
async def bot_start(message: types.Message):
    referral = message.get_args()
    if referral:
        await commands.add_user(user_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
        bot_username = (await bot.get_me()).username
        id_referral = (await commands.get_id(user_id=message.from_user.id)).id
        bot_link = f'https://t.me/{bot_username}?start={id_referral}'
        count = await commands.count_users()
        await message.answer(f'{message.from_user.get_mention()} вы перешли по реферальной ссылке'
                             f' и были доваблены в базу данных.\n'
                             f'В базе <b>{count}</b> пользователей.\n'
                             f'Твоя реферальная ссылка: {bot_link}'
                             )
        await commands.add_referral(id=id_referral, referrer_id=referral)
    else:
        await message.answer(f'Привет, {message.from_user.get_mention()}!'
                             f'Чтобы использовать этого бота введите код приглашения, либо пройдите'
                             f' по реферальной ссылке',
                             reply_markup=enter_code)


@dp.callback_query_handler(text='code')
async def enter_code_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите код доступа')
    await state.set_state('enter_code')


@dp.message_handler(state='enter_code')
async def get_code(message: types.Message, state: FSMContext):
    code = message.text
    if code in SECRET_CODE:
        await commands.add_user(user_id=message.from_user.id,
                                full_name=message.from_user.full_name,
                                username=message.from_user.username)
        bot_username = (await bot.get_me()).username
        id_referral = (await commands.select_user(user_id=message.from_user.id)).id
        bot_link = f'https://t.me/{bot_username}?start={id_referral}'
        count = await commands.count_users()
        await message.answer(f'{message.from_user.get_mention()} вы ввели код: {code} и были доваблены в базу данных.\n'
                             f'В базе <b>{count}</b> пользователей.\n'
                             f'Твоя реферальная ссылка: {bot_link}'
                             )
    else:
        await message.answer(f'Такого кода не существует, попробуйте ещё раз.', reply_markup=enter_code)

    await state.finish()
