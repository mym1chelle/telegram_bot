# Generated by Django 4.0.4 on 2022-05-28 13:26

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Название товара')),
                ('photo', models.CharField(max_length=200, verbose_name='Фото file_id')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('description', models.TextField(max_length=3000, null=True, verbose_name='Описание товара')),
                ('category_code', models.CharField(max_length=20, verbose_name='Код категории')),
                ('category_name', models.CharField(max_length=20, verbose_name='Название категории')),
                ('subcategory_code', models.CharField(max_length=20, verbose_name='Код подкатегории')),
                ('subcategory_name', models.CharField(max_length=20, verbose_name='Название подкатегории')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referrer_id', models.BigIntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Реферал',
                'verbose_name_plural': 'Рефералы',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField(default=1, unique=True, verbose_name='ID пользователя телеграм')),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('username', models.CharField(max_length=100, null=True, verbose_name='Username Телеграм')),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Email')),
                ('referrer_number', models.CharField(max_length=100)),
                ('referral', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usermanage.referral')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Стоимость')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('purchase_time', models.DateTimeField(auto_now_add=True, verbose_name='Время покупки')),
                ('shipping_address', jsonfield.fields.JSONField(null=True, verbose_name='Адрес доставки')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Номер телефона')),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Email')),
                ('reciever', models.CharField(max_length=100, null=True, verbose_name='Имя получателя')),
                ('successful', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('buyer', models.ForeignKey(on_delete=models.SET(0), to='usermanage.user', verbose_name='Покупатель')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanage.item', verbose_name='Идентификатор товара')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
    ]
