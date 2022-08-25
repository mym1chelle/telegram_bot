from utils.misc.check_channel import check
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.menu_keyboard import buy_item_keyboard
from keyboards.inline.start_keyboard import start_keyboard

from utils.db_api import db_commands as commands
from loader import dp, bot
import random


from data.config import CHANNEL, SECRET_CODE
from keyboards.inline.enter_code import enter_code

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """Функция является основным инструментом регистрации пользователей
    Для начала проверяет вдруг пользователь уже зарегестрирован. Если это так, то при нажатии команды /start выдает ему меню.
    Если пользователь не зарегестрирован, а просто нажал команду /start то бот отправляет ему сообщение с инструкцией о том, как можно зарегестрироваться:
    1. Ввести секретный код
    Пользователь нажимает инлайн-кнопку и вводит код, если код неверный, то пользователю предлагается повторить попытку. Если код верный, то пользователя добавляют в базу данных
    и дают ему реферальную ссылку по которой могут регестрироваться другие пользователи
    2. Подписаться на канал
    Пользователь может подписаться на канал, в таком случае при нажатии кнопки для проверки подписки пользователь будет зарегистрирован.
    
    Пользователь также может быть зарегистрирован если перейдет по реферальной ссылке другого пользователя, который уже зарегестрирован в БД.
    Это работает так:
    - Пользователь преходит по реферальной ссылке. Осуществляется проверка: есть ли среди зарегестрированных пользователь такой, у которого ссылка, по которой перешел новый пользователь.
    Если нет, то отправляем сообщение о том, что реферальная ссылка не верная.
    Если пользователь с такой реферальной ссылкой существует, то ему начисляется бонус за переход по его ссылке. Далее, чтобы считать сколько пользователей было зарегестрировано с помощью реферальной ссылки
    добавляем пользователя в список рефералов и берем его id, либо (если такой пользователь уже есть в списке) берем его id.
    - Регистрируем нового пользователя.
    """
    
    get_user = await commands.select_user(user_id=message.from_user.id) # пытаюсь найти пользователя с текущим user_id в базе данных

    if get_user == False: # если пользователя с таким user_id в базе данных нет, то проверяю передавал ли при запуске бота пользователь аргумент
        referral = message.get_args()

        if referral: # если аргумент был передан, проверяю есть ли пользователь в базе данных у которого такая реферральная ссылка
            check = await commands.get_referrer(referrer_number=referral)

            if check: # если пользователь с такой реферральной ссылкой найден
                await commands.add_bonus(user_id=check.user_id) # начисляю данному пользователю бонус за переход по его реферальной ссылке
                code_ref = int(message.from_user.id + random.randrange(1, 10)) # создаю реферальную ссылку для нового пользователя
                ref = await commands.add_referral(referral_id=referral) # добавляю пользователя, по чьей ссылке перешли, в таблицу рефералов, если он не зарегестрирован там. Если он там есть - беру его id
                await commands.add_user(user_id=message.from_user.id,
                            full_name=message.from_user.full_name,
                            username=message.from_user.username, 
                            referrer_number=code_ref, 
                            referral=int(ref))

        
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
            chat = await bot.get_chat(chat_id=CHANNEL) # собираю информацию о канале по его id
            invite_link = await chat.export_invite_link() # создаю ссылку для приглашения в этот канал
            channel_format = f'Канал <a href="{invite_link}">{chat.title}</a>\n\n'

            await message.answer(f'Привет, {message.from_user.get_mention()}!'
                                f'Чтобы использовать этого бота введите код приглашения, либо пройдите'
                                f' по реферальной ссылке.'
                                f'Если у вас нет ссылки и кода, то подпишитесь на канал: \n'
                                f'{channel_format}',
                                reply_markup=enter_code, disable_web_page_preview=True)
    else:
        item_id = message.get_args()
        if item_id:
            item = await commands.get_item(item_id=item_id)
            if item:
                await message.answer(f'Название товара: {item.name}\n'
                            f'Цена: {item.price}\n', reply_markup=buy_item_keyboard(item_id=item.id))
            else:
                await message.answer('Меню:', reply_markup=start_keyboard)
        else:
            await message.answer('Меню:', reply_markup=start_keyboard)



@dp.callback_query_handler(text='ref')
async def view_referral(call: types.CallbackQuery):
    """Функция выводит в сообщении сколько пользователей было зарегистрированно благодаря реферральной ссылке пользователя"""
    await call.answer()
    referrals = await commands.view_referral(user_id=call.from_user.id)
    bonus = (await commands.select_user(user_id=call.from_user.id)).bonus
    try:
        if referrals:
            await call.message.edit_text(f'{call.from_user.get_mention()}, по вашей реферальной ссылке было зарегистрировано пользователей - {referrals}. \n'
            f'Количество бонусных баллов: {bonus}', reply_markup=start_keyboard)
        else:
            await call.message.edit_text(f'{call.from_user.get_mention()}, по вашей реферальной ссылке ни один пользователь не зарегестрирован.', reply_markup=start_keyboard)
    except:
        pass


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

        ref_id = await commands.add_referral(referral_id=code)
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
    status = await check(user_id=call.from_user.id, channel=CHANNEL)
    channel = await bot.get_chat(CHANNEL)
    bot_username = (await bot.get_me()).username
    code_ref = int(call.from_user.id + random.randrange(1, 10))
    bot_link = f'https://t.me/{bot_username}?start={code_ref}'
    if status:
        await call.message.answer(f'Подписка на канал <b>{channel.title}</b> оформлена!\n\n')

        ref_id = await commands.add_referral(referral_id=CHANNEL)
    
        await commands.add_user(user_id=call.from_user.id,
                            full_name=call.from_user.full_name,
                            username=call.from_user.username,
                            referrer_number=code_ref,
                            referral=ref_id)

        count = await commands.count_users()
        await call.message.answer(f'{call.from_user.get_mention()} вы оформили подписку на канал и были доваблены в базу данных.\n'
                         f'В базе <b>{count}</b> пользователей.\n'
                         f'Твоя реферальная ссылка: {bot_link}'
                         )
    else:
        invite_link = channel.export_invite_link()
        await call.message.answer(f'Подписка на канал <b>{channel.title}</b> не оформлена!\n'\
                    f'<a href="{invite_link}">Нужно подписаться</a>', disable_web_page_preview=True)
