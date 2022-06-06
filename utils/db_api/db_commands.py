from django_project.telegrambot.usermanage.models import Item, User, Referral, BotAdmin  # импортирую модели
# функции по работе с SQL запросами у нас будут синхронными, так сам джанго работает синхронно
# для того чтобы заставить данные функции работать асинхронно с aiogram используем библиотеку asgiref
from asgiref.sync import sync_to_async

from typing import List


@sync_to_async
def select_user(user_id: int):
    try:
        return User.objects.get(user_id=user_id)
    except:
        return False
        
@sync_to_async
def get_referrer(referrer_number: int):
    try:
        return User.objects.get(referrer_number=referrer_number)
    except:
        return False

@sync_to_async  # будем таким образом преобразовывать синхронную функцию в асинхронную
def add_user(user_id, full_name, username, referrer_number, referral):
    try:
        return User(user_id=int(user_id), name=full_name, username=username, referrer_number=referrer_number, referral_id=referral).save()
    except Exception:
        print('ошибка')
        return select_user(int(user_id))


@sync_to_async
def select_all_users() -> List[User]:
    # добавил тут distinct
    return User.objects.all()


@sync_to_async
def count_users():
    return User.objects.all().count()


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
def add_referral(referral_id):
    try:
        Referral(referrer_id=referral_id).save()
        return Referral.objects.get(referrer_id=int(referral_id)).id
    except Exception:
        return Referral.objects.get(referrer_id=int(referral_id)).id


@sync_to_async
def view_referral(user_id: int):
    try:
        referrer_number = User.objects.get(user_id=user_id).referrer_number
        get_referral = Referral.objects.get(referrer_id=referrer_number)
        
        return get_referral.user_set.all().count()
    except:
        False


@sync_to_async
def add_bonus(user_id: int):
    user = User.objects.get(user_id=user_id)
    user_bonus_new = user.bonus + 10
    user.bonus = user_bonus_new
    user.save()
    return 'Бонус зачислен'
    



@sync_to_async
def get_admin(user_id):
    try:
        return BotAdmin.objects.get(user_id=user_id)
    except:
        return False


@sync_to_async
def add_item(name, price, description, category_code, category_name, subcategory_code, subcategory_name):
    try:
        Item(name=name, price=price, description=description, category_code=category_code, category_name=category_name, subcategory_code=subcategory_code, subcategory_name=subcategory_name).save()
    except:
        print('Ошибка')