# Generated by Django 2.2 on 2019-11-28 23:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guantapp', '0003_auto_20191128_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Teléfono inválido', regex='[267][0-9]{7}')]),
        ),
    ]
