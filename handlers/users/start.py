from utils.misc.check_channel import check
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command
from keyboards.inline.start_keyboard import start_keyboard
from utils.db_api import db_commands as commands
from loader import dp, bot
from filters import UserFilter
import random


from data.config import CHANNEL, SECRET_CODE
from keyboards.inline.enter_code import enter_code
from states import AddItems

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """Функция выполняет все проверки зарегистрирован ли пользователь и регистрацию пользователя в базе данных при обращении к боту в первый раз"""
    get_user = await commands.select_user(user_id=message.from_user.id) # пытаюсь найти пользователя с текущим user_id в базе данных

    if get_user == False: # если пользователя с таким user_id в базе данных нет, то проверяю передавал ли при запуске бота пользователь аргумент
        referral = message.get_args()

        if referral: # если аргумент был передан, проверяю есть ли пользователь в базе данных у которого такая реферральная ссылка
            check = await commands.get_referrer(referrer_number=referral)

            if check: # если пользователь с такой реферральной ссылкой найден
                await commands.add_bonus(user_id=check.user_id) # начисляю данному пользователю бонус за переход по его рефферальной ссылке
                code_ref = int(message.from_user.id + random.randrange(1, 10)) # создаю реферральную ссылку для нового пользователя
                check_ref = await commands.select_referral(referrer_id=referral) # проверяю есть ли в списке ссылок, по которым переходили раньше пользователи, ссылка на пользователя с рефферальной ссылкой при запуске бота
                
                if check_ref == False: # если там нет этого пользователя, добавляю
                    await commands.add_referral(referral_id=referral)
                    
                    ref_id = await commands.select_referral(referrer_id=referral) # и тут же беру его id чтобы зарегестрировать нового пользователя в базе данных и связать их, так как регистрация прошла благодаря переходу по его рефферальной ссылке

                    await commands.add_user(user_id=message.from_user.id,
                            full_name=message.from_user.full_name,
                            username=message.from_user.username, referrer_number=code_ref, referral=ref_id)



                else:
                    # по ссылке уже переходили другие пользователи второй раз этого пользователя в список реферралов не добавляем
                    await commands.add_user(user_id=message.from_user.id,
                            full_name=message.from_user.full_name,
                            username=message.from_user.username, 
                            referrer_number=code_ref, 
                            referral=int(check_ref))

        
                bot_username = (await bot.get_me()).username
        
        
                bot_link = f'https://t.me/{bot_username}?start={code_ref}'
                count = await commands.count_users()
                await message.answer(f'{message.from_user.get_mention()} вы перешли по реферальной ссылке'
                                f' и были доваблены в базу данных.\n'
                                f'В базе <b>{count}</b> пользователей.\n'
                                f'Твоя реферальная ссылка: {bot_link}'
                                )
            else:
                await message.answer(f'{message.from_user.get_mention()} такой реферальной ссылки не существует.')

        else:
            await message.answer(f'Привет, {message.from_user.get_mention()}!'
                                f'Чтобы использовать этого бота введите код приглашения, либо пройдите'
                                f' по реферальной ссылке',
                                reply_markup=enter_code)
    else:
        await message.answer('Меню:', reply_markup=start_keyboard)


@dp.callback_query_handler(text='ref')
async def view_referral(call: types.CallbackQuery):
    """Функция выводит в сообщении сколько пользователей было зарегестрированно благодаря реферральной ссылке пользователя"""
    await call.answer()
    referrals = await commands.view_referral(user_id = call.from_user.id)
    if referrals:
        await call.message.answer(f'{call.from_user.get_mention()}, по вашей реферальной ссылке было зарегистрировано пользователей - {referrals}')
    else:
        await call.message.answer(f'{call.from_user.get_mention()}, по вашей реферальной ссылке ни один пользователь не зарегестрирован.')


@dp.callback_query_handler(text='code')
async def enter_code_handler(call: types.CallbackQuery, state: FSMContext):
    """Функция отвечает за ввод кода от пользователя и его проверку и при корректном вводе его регистрации в базе данных.
    Функция разделена на два этапа: enter_code_handler и get_code.
    Ввод кода реализуется через машину состояний. Так как мне не нужно сохранять информацию, а сразу могу брать ее из сообщения, то я отдельно не прописываю состояния и не сохраняю их."""
    await call.message.answer('Введите код доступа')
    await state.set_state('enter_code')


@dp.message_handler(state='enter_code')
async def get_code(message: types.Message, state: FSMContext):
    code = message.text

    if code in SECRET_CODE:  # проверка на корректность введенного кода
        code_ref = int(message.from_user.id + random.randrange(1, 10))

        await commands.add_referral(referral_id=code)
        ref_id = await commands.select_referral(referrer_id=code)
        print(f'{message.from_user.id}, {message.from_user.full_name}, {message.from_user.username}, {code_ref}, {ref_id}')
        await commands.add_user(user_id=message.from_user.id,
                            full_name=message.from_user.full_name,
                            username=message.from_user.username,
                            referrer_number=code_ref,
                            referral=ref_id)

        bot_username = (await bot.get_me()).username
        bot_link = f'https://t.me/{bot_username}?start={code_ref}'
        count = await commands.count_users()
        await message.answer(f'{message.from_user.get_mention()} вы ввели код: {code} и были доваблены в базу данных.\n'
                         f'В базе <b>{count}</b> пользователей.\n'
                         f'Твоя реферальная ссылка: {bot_link}'
                         )
    else:
        await message.answer(f'Такого кода не существует, попробуйте ещё раз.', reply_markup=enter_code)

    await state.finish()


@dp.callback_query_handler(text='check_subs')
async def check_subs(call: types.CallbackQuery):
    """Данная функция отвечает за проверку подписки на канал у пользователя, что нажал на кнопку"""
    await call.answer()
    result = str()
    status = await check(user_id=call.from_user.id, channel=CHANNEL)
    channel = await bot.get_chat(CHANNEL)
    if status:
        result += f'Подписка на канал <b>{channel.title}</b> оформлена!\n\n'
    else:
        invite_link = channel.export_invite_link()
        result += f'Подписка на канал <b>{channel.title}</b> не оформлена!\n'\
                    f'<a href="{invite_link}">Нужно подписаться</a>'

    await call.message.answer(result, disable_web_page_preview=True)



# Последующий блок функций реализует добавление товара через бота. Чтобы не каждый пользователь имел ввозможность добавлять товар, в базе данных создана таблица администраторов, откуда реализует работу фильтр
@dp.message_handler(Command('add_item'), UserFilter())
async def add_item(message: types.Message):
    await message.answer('Название товара')
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
    
  
    await commands.add_item(name=item_name, price=item_price, description=item_description, category_code=item_category_code, category_name=item_category_name, subcategory_code=item_subcategory_code, subcategory_name=item_subcategory_name)

    await state.finish()