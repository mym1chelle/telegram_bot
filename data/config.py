from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
HOST = env.str("ip")  # Тоже str, но для айпи адреса хоста
NAME = env.str('NAME_DB')
USER = env.str('USER_DB')
PASSWORD = env.str('PASSWORD_DB')
PORT = env.str('PORT')
SECRET_CODE = env.list('SECRET_CODE')
CHANNEL=env.int('CHANNELS')
