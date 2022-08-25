from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import db_commands as commands


class AdminFilter(BoundFilter):  # тестовый фильтр для проверки пользователя в списке админов
    async def check(self, message: types.Message) -> bool:
        user = await commands.get_admin(user_id=message.from_user.id)
        if user:
            return True
        else:
            await message.answer('У вас недостаточно прав, чтобы использовать данную функцию')
            return False
