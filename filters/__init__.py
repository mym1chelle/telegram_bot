from aiogram import Dispatcher

from loader import dp
from .is_admin import UserFilter


if __name__ == "filters":
    dp.filters_factory.bind(UserFilter)