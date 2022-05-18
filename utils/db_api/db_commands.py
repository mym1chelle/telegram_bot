# я создал отдельную директорию для этого файла лишь потому, что у меня куча других файлов и я начинаю путаться

from django_project.telegrambot.usermanage.models import Item, User, Referral  # импортирую модели
# функции по работе с SQL запросами у нас будут синхронными, так сам джанго работает синхронно
# для того чтобы заставить данные функции работать асинхронно с aiogram используем библиотеку asgiref
from asgiref.sync import sync_to_async

from typing import List


@sync_to_async
def select_user(user_id: int):
    return User.objects.filter(user_id=user_id).first()


@sync_to_async  # будем таким образом преобразовывать синхронную функцию в асинхронную
def add_user(user_id, full_name, username):
    try:
        return User(user_id=int(user_id), name=full_name, username=username).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def select_all_users() -> List[User]:
    # добавил тут distinct
    return User.objects.all()


@sync_to_async
def count_users():
    return User.objects.all().count()


@sync_to_async
def add_item(**kwargs):
    """функция добавления товара не через django админку"""
    newitem = Item(**kwargs).save()
    return newitem


@sync_to_async
def get_categories() -> List[Item]:
    return Item.objects.distinct('category_code').all()


@sync_to_async
def get_subcategories(category_code) -> List[Item]:
    return Item.objects.distinct('subcategory_name').filter(category_code=category_code).all()


@sync_to_async
def count_items(category_code, subcategory_code=None) -> int:
    conditions = dict(category_code=category_code)  # словарь условий
    if subcategory_code:
        conditions.update(subcategory_code=subcategory_code)
    return Item.objects.filter(**conditions).count()


@sync_to_async
def get_items(category_code, subcategory_code) -> List[Item]:
    return Item.objects.filter(category_code=category_code, subcategory_code=subcategory_code).all()


@sync_to_async
def get_item(item_id):
    return Item.objects.filter(id=int(item_id)).first()


@sync_to_async
def get_all_items() -> List[Item]:
    # получаю список названий всеъ товаров (для работы в инлайн режиме не использую эту функцию)
    return Item.objects.distinct('name').all()


@sync_to_async
def search_item(text: str) -> List[Item]:
    # осуществляю поиск по введенному тексту среди имён товаров и сортирую в алфавитном порядке
    return Item.objects.filter(name__icontains=text).all().order_by(
        'name')  # не понял разницу между __сontains и __icontains


@sync_to_async
def select_referral(id):
    return Referral.objects.filter(id_id=int(id)).first()


@sync_to_async
def add_referral(id, referrer_id):
    try:
        return Referral(id_id=id, referrer_id=referrer_id).save()
    except Exception:
        return select_referral(id=id)










