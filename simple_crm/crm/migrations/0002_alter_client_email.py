# Generated by Django 3.2.8 on 2021-10-29 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=255, null=True),
        ),
    ]
