from django.db import models
from jsonfield import JSONField


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True  # абстрактный метод на основании которого будут создаваться все остальные
    # создаем две колонки, как и в случае с Gino (чтобы видеть дату создания строки в БД и дату изменения)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModel):
    """таблица пользователей"""
    class Meta:
        verbose_name = 'Пользователь'  # название одной строки
        verbose_name_plural = 'Пользователи' # название таблицы

    # создание полей тут более явное чем в Gino
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name='ID пользователя телеграм') # verbose_name – название колонки
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    username = models.CharField(max_length=100, verbose_name='Username Телеграм')
    email = models.CharField(max_length=100, verbose_name='Email', null=True)  # null=True — поле может быть пустым

    def __str__(self):
        # метод для принта пользователя
        return f'№{self.id} ({self.user_id} — {self.name})'
        # return f'{self.id}'


class Referral(TimeBasedModel):
    class Meta:
        verbose_name = 'Реферал'
        verbose_name_plural = 'Рефералы'
    # id того, кто перешел по ссылке
    id = models.ForeignKey(User, unique=True, primary_key=True, on_delete=models.CASCADE)  # связываем по этому ключу с таблицей User
    # on_delete=models.CASCADE – при удалении пользователя из таблицы User это же пользователь удалится из этой таблицы
    referrer_id = models.BigIntegerField()  # id того, чья была ссылка

    def __str__(self):
        return f'№{self.id} — от {self.referrer_id}'


class Item(TimeBasedModel):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название товара', max_length=50)
    photo = models.CharField(verbose_name='Фото file_id', max_length=200)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=8)
    # используем тип поля с достаточной точностью приближения
    # decimal_places – знаки после запятой
    # max_digits – всего знаков с теми, что после запятой
    description = models.TextField(verbose_name='Описание товара', max_length=3000, null=True)

    category_code = models.CharField(verbose_name='Код категории', max_length=20)
    category_name = models.CharField(verbose_name='Название категории', max_length=20)
    subcategory_code = models.CharField(verbose_name='Код подкатегории', max_length=20)
    subcategory_name = models.CharField(verbose_name='Название подкатегории', max_length=20)

    def __str__(self):
        return f'№{self.id} — {self.name}'


class Purchase(TimeBasedModel):
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.SET(0))
    # если из таблицы User удалился пользователь, то в этой колонке будет стоять 0
    item_id = models.ForeignKey(Item, verbose_name='Идентификатор товара', on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='Стоимость', decimal_places=2, max_digits=8)
    quantity = models.IntegerField(verbose_name='Количество')
    purchase_time = models.DateTimeField(verbose_name='Время покупки', auto_now_add=True)
    shipping_address = JSONField(verbose_name='Адрес доставки', null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=50)
    email = models.CharField(verbose_name='Email', max_length=100, null=True)
    reciever = models.CharField(verbose_name='Имя получателя', max_length=100, null=True)
    successful = models.BooleanField(verbose_name='Оплачено', default=False)

    def __str__(self):
        return f'№{self.id} — {self.item_id} ({self.quantity})'