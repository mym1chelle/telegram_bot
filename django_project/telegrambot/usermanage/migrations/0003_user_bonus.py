# Generated by Django 4.0.4 on 2022-05-30 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0002_alter_item_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bonus',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Цена'),
        ),
    ]
