# Generated by Django 3.2.8 on 2021-11-02 21:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cstmgmnt', '0011_auto_20211102_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientproductthrough',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 2, 21, 46, 17, 68308, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salespersonproduct',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 2, 21, 46, 17, 70368, tzinfo=utc)),
        ),
    ]
