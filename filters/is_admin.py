from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import db_commands as commands


class UserFilter(BoundFilter):  # тестовый фильтр для проверки пользователя в списке админов
    async def check(self, message: types.Message) -> bool:
        # делаю проверку
        users = await commands.select_all_users()
        users_id_list = [user.user_id for user in users]  # список всех id из бд
        for user in users_id_list:
            # делаю условия наоборот: чтобы выявлеть тех, кого нет в БД
            if message.from_user.id == int(user):
                return False
            else:
                return True


