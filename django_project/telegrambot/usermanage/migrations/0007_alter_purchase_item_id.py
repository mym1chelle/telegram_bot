# Generated by Django 4.0.4 on 2022-07-10 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0006_alter_purchase_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='item_id',
            field=models.ForeignKey(on_delete=models.SET('-'), to='usermanage.item', verbose_name='Идентификатор товара'),
        ),
    ]
