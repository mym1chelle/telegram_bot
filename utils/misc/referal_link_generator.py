# ^id[a-zA-Z0-9]{11}$ – на будущее, чтобы сделать ссылку крутой
# пока я просто буду брать 4 рандомных числа
import random


def gen_ref_link():
    return random.randint(1000, 10000)