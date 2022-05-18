from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from utils.db_api.db_commands import add_user


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    id = await add_user(message.from_user.id)
    chat_id = message.from_user.id
    referral = message.get_args()
    bot_username = (await bot.get_me()).username
    id_referral = id
    bot_link = f'https://t.me/{bot_username}?start={id_referral}'