# Generated by Django 4.0.4 on 2022-06-02 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0003_user_bonus'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotAdmin',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('user_id', models.BigIntegerField(default=1, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
