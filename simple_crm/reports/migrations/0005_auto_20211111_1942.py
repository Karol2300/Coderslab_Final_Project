# Generated by Django 3.2.8 on 2021-11-11 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20211101_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='balcony',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='loggia',
            field=models.BooleanField(default=False),
        ),
    ]