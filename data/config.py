from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  
ADMINS = env.list("ADMINS")  
HOST = env.str("ip")  
NAME = env.str('NAME_DB')
USER = env.str('USER_DB')
PASSWORD = env.str('PASSWORD_DB')
PORT = env.str('PORT')
SECRET_CODE = env.list('SECRET_CODE')
CHANNEL = env.int('CHANNELS')
BOT_LINK = env.str('BOT_LINK')

# для оплаты
PROVIDER_TOKEN = env.str('PROVIDER_TOKEN')

# для тестирования веб-приложения
APP_LINK = env.str('APP_LINK')