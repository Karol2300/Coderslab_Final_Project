# Generated by Django 3.2.8 on 2021-11-11 20:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cstmgmnt', '0018_auto_20211111_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientproductthrough',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 20, 48, 34, 345911, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salespersonproduct',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 20, 48, 34, 348030, tzinfo=utc)),
        ),
    ]
