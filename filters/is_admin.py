from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import db_commands as commands


class UserFilter(BoundFilter):  # тестовый фильтр для проверки пользователя в списке админов
    async def check(self, message: types.Message) -> bool:
        user = await commands.get_admin(user_id=message.from_user.id)
        if user:
            return True
        else:
            return False


