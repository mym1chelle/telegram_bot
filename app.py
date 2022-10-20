import os

import django


# from loader import db
# from utils.db_api.db_gino_big_menu import create_db
from utils.set_bot_commands import set_default_commands
# from utils.db_api import db_gino
import logging


async def on_startup(dp):
    import filters
    import middlewares

    from utils.notify_admins import on_startup_notify
    # # Для SQLite
    # try:
    #     db.create_table_users()  # создаём БД
    # except Exception as err:
    #     print(err)
    # db.delete_users()  # если БД уже была создана, то чистим её
    # print(db.select_all_users())

    # # Для PostgreSQL
    # logging.info('Создаём подключение к PostgreSQL')
    # await db.create() # создаём подключение к БД
    #
    # await db.drop_users() # удаляем таблицу, если она есть
    # logging.info('Создаём таблицу Users')
    # await db.create_table_users()
    # logging.info('Готово')
    #
    # Уведомляет про запуск
    await on_startup_notify(dp)
    # Показывает подсказки по коммандам
    await set_default_commands(dp)

    # # для Gino
    # print('Подключаем БД')
    # await db_gino.on_startup(dp)
    # print('Готово')
    #
    # print('Чистим БД')
    # await db.gino.drop_all()
    # print('Готово')
    #
    # print('Создаём таблицы')
    # await db.gino.create_all()
    # print('Готово')

    # для многоуровневого меню
    # await create_db()


def setup_django():
    # передаю новую переменную окружения
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.telegrambot.telegrambot.settings')
    # разрешаю джанго использовать асинхронные функции
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
    django.setup()


if __name__ == '__main__':
    setup_django()

    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)

# #  для работы с Webhook и подключением к БД на сервере через Gino
# from loader import db
# from utils.db_api import db_gino
# from aiogram.utils.executor import start_webhook
#
# from data.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
# from loader import bot, SSL_CERTIFICATE, ssl_context
# from utils.set_bot_commands import set_default_command
#
#
# async def on_startup(dp):
#     # по старту бота запускаем метот setWebhook
#     await bot.set_webhook(
#         url=WEBHOOK_URL,
#         certificate=SSL_CERTIFICATE
#     )
#
#     import filters
#     import middlewares
#     filters.setup(dp)
#     middlewares.setup(dp)
#
#     from utils.notify_admins import on_startup_notify
#     # Уведомляет про запуск
#     await on_startup_notify(dp)
#     # Показывает подсказки по коммандам
#     await set_default_command(dp)
#
#     # для Gino
#     print('Подключаем БД')
#     await db_gino.on_startup(dp)
#     print('Готово')
#
#     print('Чистим БД')
#     await db.gino.drop_all()
#     print('Готово')
#
#     print('Создаём таблицы')
#     await db.gino.create_all()
#     print('Готово')
#
# if __name__ == '__main__':
#     from handlers import dp
#
#     start_webhook(
#         dispatcher=dp,
#         webhook_path=WEBHOOK_PATH,
#         on_startup=on_startup,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#         ssl_context=ssl_context
#     )
