from loader import dp
from aiogram import types


# эта функция ненужная, удалить
@dp.message_handler()
async def get_message(message: types.Message):
    user = message.from_user.full_name
    message = message.text
    print(user, message)


