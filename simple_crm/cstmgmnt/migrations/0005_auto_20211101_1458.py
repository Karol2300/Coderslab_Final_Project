# Generated by Django 3.2.8 on 2021-11-01 14:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cstmgmnt', '0004_auto_20211030_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesperson',
            name='full_name',
        ),
        migrations.AlterField(
            model_name='clientproductthrough',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 1, 14, 58, 42, 543992, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salespersonproduct',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 1, 14, 58, 42, 546049, tzinfo=utc)),
        ),
    ]