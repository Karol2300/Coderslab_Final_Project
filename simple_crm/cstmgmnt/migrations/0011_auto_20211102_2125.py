# Generated by Django 3.2.8 on 2021-11-02 21:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cstmgmnt', '0010_auto_20211102_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientproductthrough',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 2, 21, 25, 51, 664425, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salespersonproduct',
            name='date_of_link',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 2, 21, 25, 51, 666570, tzinfo=utc)),
        ),
    ]