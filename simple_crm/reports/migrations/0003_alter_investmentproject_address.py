# Generated by Django 3.2.8 on 2021-11-01 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20211030_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentproject',
            name='address',
            field=models.CharField(max_length=255),
        ),
    ]