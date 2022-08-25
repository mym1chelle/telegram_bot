
from decimal import Decimal
from django_project.telegrambot.usermanage.models import Item, Purchase, User, Referral, BotAdmin
from asgiref.sync import sync_to_async
from django.db.models import Sum, Count

from typing import List


@sync_to_async
def select_user(user_id: int):
    """Выбор пользователя по его id"""
    try:
        return User.objects.get(user_id=user_id)
    except:
        return False
        
@sync_to_async
def get_referrer(referrer_number: int):
    """Выбор пользователя по его реферальной ссылке"""
    try:
        return User.objects.get(referrer_number=referrer_number)
    except:
        return False

@sync_to_async
def add_user(user_id, full_name, username, referrer_number, referral):
    """Добавление нового пользователя"""
    try:
        return User(user_id=int(user_id), name=full_name, username=username, referrer_number=referrer_number, referral_id=referral).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def select_all_users() -> List[User]:
    """Выбор всех польователей"""
    return User.objects.all()


@sync_to_async
def count_users():
    """Посчитать число пользователей в базе данных"""
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
    """Добавление пользователя в таблицу рефералов. Если пользователь уже там есть,
    то выбирает его из таблицы"""
    try:
        Referral(referrer_id=referral_id).save()
        return Referral.objects.get(referrer_id=int(referral_id)).id
    except Exception:
        return Referral.objects.get(referrer_id=int(referral_id)).id


@sync_to_async
def view_referral(user_id: int):
    """Показывает сколько пользователей зарегистрировалось по реферальной ссылке данного пользователя"""
    try:
        referrer_number = User.objects.get(user_id=user_id).referrer_number
        get_referral = Referral.objects.get(referrer_id=referrer_number)
        return get_referral.user_set.all().count()
    except:
        False


@sync_to_async
def add_bonus(user_id: int):
    """Начисление бонусов пользователю"""
    user = User.objects.get(user_id=user_id)
    user_bonus_new = user.bonus + 10
    user.bonus = user_bonus_new
    user.save()
    return 'Бонус зачислен'
    

@sync_to_async
def get_admin(user_id):
    """Поиск пользователя в таблице администратовров по user_id"""
    try:
        return BotAdmin.objects.get(user_id=user_id)
    except:
        return False


@sync_to_async
def add_item(name, price, description, category_code, category_name, subcategory_code, subcategory_name):
    """Добавление товаров"""
    try:
        Item(name=name, price=price, description=description, category_code=category_code, category_name=category_name, subcategory_code=subcategory_code, subcategory_name=subcategory_name).save()
    except:
        print('Ошибка')
        return False


@sync_to_async
def get_last_purchase(user_id):
    """Берет последний добавленный заказ"""
    return Purchase.objects.filter(buyer_id=user_id).last()


# @sync_to_async
# def get_purchase(purchase_id):
#     """Ищет заказ по id"""
#     return Purchase.objects.get(id=purchase_id)


@sync_to_async
def get_last_unpaid_purchase(user_id):
    """Берет последний неоплаченный заказ"""
    try:
        return Purchase.objects.filter(buyer_id=user_id).filter(successful=False).last()
    except:
        print('Ошибка')
        return False


@sync_to_async
def select_purchase(user_id):
    """Выбор всех заказов у пользователя"""
    return Purchase.objects.filter(buyer_id=user_id)

@sync_to_async
def select_unpaid_purchase(user_id):
    """Выбор всех неоплаченных заказов пользователя"""
    try:
        return Purchase.objects.filter(buyer_id=user_id).filter(successful=False)
    except:
        return False


@sync_to_async
def count_sum(user_id):
    """Выводит список заказов пользователя. Группирует их по названию и суммирует цену и количество"""
    return Purchase.objects.filter(buyer_id=user_id).values('item_id').annotate(total=Sum('amount'), quantity=Sum('quantity'))

@sync_to_async
def total_sum_unpaid_purchase(user_id):
    """Выводит сумму всех неоплаченных пользователем товаров"""
    try:
        return Purchase.objects.filter(buyer_id=user_id).filter(successful=False).aggregate(Sum('amount'))
    except:
        return False

@sync_to_async
def edit_name(item_id, new_name):
    item = Item.objects.get(id=item_id)
    print(item.name)
    print(new_name)
    item.name = new_name
    item.save()

@sync_to_async
def edit_description(item_id, new_description):
    item = Item.objects.get(id=item_id)
    print(item.description)
    print(new_description)
    item.description = new_description
    item.save()

@sync_to_async
def edit_price(item_id, new_price):
    item = Item.objects.get(id=item_id)
    print(item.price)
    print(new_price)
    item.price = new_price
    item.save()

@sync_to_async
def edit_category_code(item_id, new_category_code):
    item = Item.objects.get(id=item_id)
    print(item.category_code)
    print(new_category_code)
    item.category_code = new_category_code
    item.save()

@sync_to_async
def edit_category_name(item_id, new_category_name):
    item = Item.objects.get(id=item_id)
    print(item.category_name)
    print(new_category_name)
    item.category_name = new_category_name
    item.save()

@sync_to_async
def edit_subcategory_code(item_id, new_subcategory_code):
    item = Item.objects.get(id=item_id)
    print(item.subcategory_code)
    print(new_subcategory_code)
    item.subcategory_code = new_subcategory_code
    item.save()

@sync_to_async
def edit_subcategory_name(item_id, new_subcategory_name):
    item = Item.objects.get(id=item_id)
    print(item.subcategory_name)
    print(new_subcategory_name)
    item.subcategory_name = new_subcategory_name
    item.save()

@sync_to_async
def delete_item(item_id):
    try:
        item = Item.objects.get(id=item_id)
        return item.delete()
    except:
        print('Ошибка')
        return False

@sync_to_async
def increase(purchase_id, purchase_price):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.quantity = purchase.quantity + 1
        purchase.amount = purchase.amount + Decimal(purchase_price)
        purchase.save()
    except:
        print('Ошибка')
        return False

@sync_to_async
def decrease(purchase_id, purchase_price):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.quantity = purchase.quantity - 1
        purchase.amount = purchase.amount - Decimal(purchase_price)
        purchase.save()
    except:
        print('Ошибка')
        return False

    
@sync_to_async
def change_quantity(purchase_id, purchase_quantity, purchase_price):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.quantity = purchase_quantity
        purchase.amount = Decimal(purchase_price) * purchase_quantity
        purchase.save()
    except:
        print('Ошибка')
        return False

@sync_to_async
def delete_purchase(purchase_id):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        return purchase.delete()
    except:
        print('Ошибка')
        return False


# это тестовая функция
@sync_to_async
def select_all_purchase():
    """Выбор всех заказов у всех пользователей"""
    return Purchase.objects.all()

@sync_to_async
def get_purchase(purchase_id):
    return Purchase.objects.get(id=purchase_id)