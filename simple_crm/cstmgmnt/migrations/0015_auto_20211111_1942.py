# Generated by Django 3.2.8 on 2021-11-11 19:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cstmgmnt', '0014_auto_20211104_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientproductthrough',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 19, 42, 31, 133418, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salespersonproduct',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 19, 42, 31, 135509, tzinfo=utc)),
        ),
    ]
